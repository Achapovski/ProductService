from abc import ABC, abstractmethod
from typing import Any


class AbstractBrokerClient(ABC):
    def __init__(self, broker_url: str) -> None:
        self.broker_url = broker_url

    @abstractmethod
    async def consume(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, payload: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_message(self, *args) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

