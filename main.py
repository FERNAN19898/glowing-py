import os
import json
import asyncio
import importlib

from tabulate import tabulate
from core.own_logger import Logger
from core.ddp_client import DDPClient
from pynput.keyboard import Listener, Key
from plugins.registered_plugins import registered_plugins

log = Logger()

class GlowingPyEngine:
    def __init__(self):
        log.info("Starting GlowingPy Engine...")

        self.config = self._load_config()
        self.ddp = DDPClient(self.config["wled_ip"])
        self.led_count = self.config["led_count"]

        self.loop_task = None
        self.cur_plugin_task = None
        
        self.state = "MENU"
        self.stop_plugin_requested = False

        # Setup F7 keyboard listener to stop current plugin
        def _on_press(key):
            try:
                if key == Key.f7 and self.state != "MENU":
                    if self.cur_plugin_task and not self.cur_plugin_task.done():
                        log.info("F7 pressed — requesting stop plugin task...")
                        self.stop_plugin_requested = True

            except Exception as e:
                log.debug(f"Keyboard listener error: {e}")

        self._kb_listener = Listener(on_press=_on_press)
        self._kb_listener.daemon = True
        self._kb_listener.start()

    def _load_config(self):
        if not os.path.exists("config.json"):
            log.error("config.json file not found.")
            raise FileNotFoundError("config.json is missing")
        with open("config.json", "r") as f:
            return json.load(f)

    async def setup(self):
        await self.start()  # Esperar a que termine el init para arrancar el loop

        async def setup_loop():
            while True:
                await self.loop()

        self.loop_task = asyncio.create_task(setup_loop())
        while not self.loop_task.done():
            await asyncio.sleep(0.1)

    async def load_plugin_by_name(self, name: str):
        # Stop any running plugin first
        await self.stop_running_plugin()

        log.info(f"Loading Plugin: {name}...")
        try:
            module = importlib.import_module(f"plugins.{name}.{name}")
            importlib.reload(module)

            cur_plugin_instance = module.Plugin(self.ddp)
            self.cur_plugin_task = asyncio.create_task(cur_plugin_instance.run())
            log.debug("loaded")
            self.state = "RUNNING"

        except ImportError:
            log.error(f"Plugin '{name}' not found. Please check the plugin name.")

        except Exception as e:
            log.error(f"Critical Error in plugin {name}: {e}")

    async def stop_running_plugin(self):
        if self.cur_plugin_task:
            try:
                self.cur_plugin_task.cancel()
                await self.cur_plugin_task
            except asyncio.CancelledError:
                pass

        self.cur_plugin_task = None
        self.state = "NOT RUNNING"

    async def start(self):
        log.clear()
        self.state = "MENU"
        
        print("========================================")
        print("       Welcome to GlowingPy Engine      ")
        print("")
        print(f"Target IP: {self.config['wled_ip']}")
        print(f"Target Port: {self.config['wled_port']}")
        print(f"Total Leds in strip: {self.led_count} LEDs")
        print("")
        print("========================================")
        print("")
        print("Select an option to begin:")
        print("1. Run a plugin by ID")
        print("2. Show Available Plugins")
        print("")
        choice = input("Enter your choice (1 or 2): ")

        if choice not in ["1", "2"]:
            log.error("Invalid input. Please enter 1 or 2.")
            await asyncio.sleep(2)
            return await self.start()
        else:
            if choice == "1":
                plugin_to_load_id = input("Enter the Plugin ID to load: ")

                try:
                    plugin_to_load_id = int(plugin_to_load_id)
                except ValueError:
                    log.error("Invalid input. Please enter a valid Plugin ID.")
                    await asyncio.sleep(3)
                    return await self.start()
                else:
                    pass

                try:
                    if plugin_to_load_id in registered_plugins:
                        log.info(
                            f"Loading Plugin {registered_plugins[plugin_to_load_id][0]}..."
                        )
                        selected_plugin = registered_plugins[plugin_to_load_id][3]
                        await self.load_plugin_by_name(selected_plugin)
                except Exception as e:
                    log.error(f"Error loading plugin: {e}")

            elif choice == "2":
                log.clear()
                log.info("Available Plugins:")
                table_data = []

                for plugin_id in registered_plugins:
                    table_data.append(
                        [
                            plugin_id,
                            registered_plugins[plugin_id][0],
                            registered_plugins[plugin_id][1],
                            registered_plugins[plugin_id][2],
                            registered_plugins[plugin_id][3],
                        ]
                    )

                headers = ["ID", "Name", "Description", "Author", "Filename"]

                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                input("\nPress Enter to return to the main menu...")
                return await self.start()

    async def loop(self):
        if self.state == "MENU":
            await asyncio.sleep(0.5)
            return
        
        if self.stop_plugin_requested:
            self.stop_plugin_requested = False
            await self.stop_running_plugin()
            await self.start()

        await asyncio.sleep(0.1)


if __name__ == "__main__":
    try:
        engine = GlowingPyEngine()
        asyncio.run(engine.setup())

    except KeyboardInterrupt:
        log.info("Shutting down GlowingPy...")
