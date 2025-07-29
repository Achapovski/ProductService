from abc import ABC, abstractmethod


class AbstractApplicationBaseException(ABC, Exception):
    EXCEPTIONS: set = set()

    def __init_subclass__(cls, **kwargs):
        cls.EXCEPTIONS.add(cls)


class AbstractExceptionHandler(ABC):
    def __init__(self, context: type[AbstractApplicationBaseException]):
        self.context: type[AbstractApplicationBaseException] = context

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError
