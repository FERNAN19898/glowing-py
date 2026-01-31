import asyncio
from ..base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Default plugin that Blinks all LEDs in three colors.
    """

    async def set_to_all_leds(self, color, delay):
        pixels = [color] * 38
        self.ddp.send_frame(pixels)
        await asyncio.sleep(delay)
        
    async def run(self):
        print("Default Plugin Started")

        try:
            while self.active:
                print("Blinking Red")
                await self.set_to_all_leds([255, 0, 0], 1)
                print("Blinking Green")
                await self.set_to_all_leds([0, 255, 0], 1)
                print("Blinking Blue")
                await self.set_to_all_leds([0, 0, 255], 1)

        except asyncio.CancelledError:
            pass

        finally:
            print("Default Plugin Stopped")