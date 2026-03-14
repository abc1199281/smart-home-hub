from abc import ABC, abstractmethod
from typing import Any


class Device(ABC):
    """Abstract base class for all smart home devices."""

    def __init__(self, name: str, host: str | None = None, **kwargs: Any):
        self.name = name
        self.host = host

    @abstractmethod
    def on(self) -> None:
        ...

    @abstractmethod
    def off(self) -> None:
        ...

    @abstractmethod
    def status(self) -> dict[str, Any]:
        ...

    def __repr__(self) -> str:
        if self.host is not None:
            return f"{self.__class__.__name__}(name={self.name!r}, host={self.host!r})"
        return f"{self.__class__.__name__}(name={self.name!r})"
