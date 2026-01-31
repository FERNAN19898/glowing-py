from abc import ABC, abstractmethod
import asyncio

class BasePlugin(ABC):
    """
    Base class that all GlowingPy effects must inherit from.
    """
    
    def __init__(self, ddp_client):
        self.ddp = ddp_client
        self.active = True

    async def stop(self):
        """Stops the plugin loop gracefully"""
        
        print(f"Stopping plugin: {self.__class__.__name__}")
        self.active = False
        await asyncio.sleep(0.1)

    @abstractmethod
    async def run(self):
        """Main loop of the plugin."""
        pass