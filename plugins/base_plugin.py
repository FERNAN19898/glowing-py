import os
import json
import asyncio

from typing import Dict, Any

from abc import ABC, abstractmethod
from core.ddp_client import DDPClient
from core.own_logger import Logger as log


class BasePlugin(ABC):
    """
    Base class that all GlowingPy plugins must inherit from.
    """

    ddp: DDPClient
    config: Dict[str, Any]

    def __init__(self, ddp_client: DDPClient):
        self.ddp: DDPClient = ddp_client
        self.config: Dict[str, Any] = {}

    def _load_config(self, foldername : str) -> Dict[str, Any]:
        config_file: str = f"plugins/{foldername}/config.json"

        if not os.path.exists(config_file):
            raise FileNotFoundError("config.json is missing")

        with open(config_file, "r") as f:
            return json.load(f)

    async def run(self, filename : str) -> None:
        log.clear()
        self.config = self._load_config(filename)
        log.info(f"{filename} Started...")
        log.debug(f"{filename} Plugin Config:")
        log.debug(self.config)
        
        try:
            await self.setup()
            while True:
                await self.loop()
        except asyncio.CancelledError:
            log.info(f"{filename} stopped")
            await self.on_stop()
            raise

    @abstractmethod
    async def setup(self) -> None:
        """Called once when the plugin starts."""
        # Your code here
        pass
    
    @abstractmethod
    async def loop(self) -> None:
        """Called every tick while the plugin is running."""
        # Your loop code here
        pass
    
    @abstractmethod
    async def on_stop(self) -> None:
        """Called once when the plugin stops."""
        pass
