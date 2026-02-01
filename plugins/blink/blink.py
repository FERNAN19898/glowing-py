from ..base_plugin import BasePlugin
from typing import List
import asyncio

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
        
        # Example: read delay from config
        self.delay: float = float(self.config["delay"])

    async def loop(self) -> None:
        """
        Called repeatedly while the plugin is running.
        Implement animation logic here.
        """
        # Example animation: blink RGB colors
        await self.fill_strip([255, 0, 0])
        await asyncio.sleep(self.delay)

        await self.fill_strip([0, 255, 0])
        await asyncio.sleep(self.delay)

        await self.fill_strip([0, 0, 255])
        await asyncio.sleep(self.delay)

    async def fill_strip(self, color: List[int]) -> None:
        """
        Fill the entire LED strip with a single color.
        """
        frame = [color] * self.ddp.led_count
        self.ddp.send_frame(frame)

    async def on_stop(self) -> None:
        """
        Called once when the plugin stops.
        Use this to reset LEDs or cleanup tasks.
        """
        await self.fill_strip([0, 0, 0])
