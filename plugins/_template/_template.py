"""
====================================
 GlowingPy Plugin Template
====================================

REQUIREMENTS
------------
1️: Folder & File Naming
   - The plugin folder and main file must have the SAME name
     Example:
       plugins/blink/blink.py
2️: Config
   - A config.json is REQUIRED in the plugin folder
   - Access values via `self.config["key"]`
3️: Async Only
   - DO NOT use time.sleep(), input(), or any blocking code
   - Always use asyncio coroutines (async def, await asyncio.sleep())
4️: Registration
   - Must be registered in `registered_plugins.py`
   - Example:
       registered_plugins[ID] = [
           "Plugin Name",
           "Short Description",
           "Author",
           "plugin_folder_name"
       ]

PLUGIN LIFECYCLE
----------------
setup()            -> called once when the plugin starts
loop()             -> called repeatedly while the plugin is running
on_plugin_stopped() -> called once when the plugin stops
"""

from ..base_plugin import BasePlugin

class Plugin(BasePlugin):
    """
    Example Plugin Template.
    Copy this folder and rename it to create a new plugin.
    """

    async def setup(self) -> None:
        """
        Called once when the plugin starts.
        Initialize variables or states here.
        """
        pass

    async def loop(self) -> None:
        """
        Called repeatedly while the plugin is running.
        Implement animation logic here.
        """
        pass

    async def on_plugin_stopped(self) -> None:
        """
        Called once when the plugin stops.
        Use this to reset LEDs or cleanup tasks.
        """
        pass
