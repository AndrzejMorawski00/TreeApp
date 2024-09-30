from abc import ABC, abstractmethod
from typing import List, Dict, Callable, Any


class IEventAggregator(ABC):
    @abstractmethod
    def add_subscriber(self, event_name: str, callback: Callable[..., Any]) -> None:
        pass

    @abstractmethod
    def remove_subscriber(self, event_name: str, callback: Callable[..., Any]) -> None:
        pass

    @abstractmethod
    def publish(self, event_name: str, *args, **kwargs) -> None:
        pass


class EventAggregator(IEventAggregator):
    def __init__(self) -> None:
        self.subscribers: Dict[str, List[Callable[..., Any]]] = {}

    def add_subscriber(self, event_name: str, callback: Callable[..., Any]) -> None:
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)

    def remove_subscriber(self, event_name: str, callback: Callable[..., Any]) -> None:
        if event_name in self.subscribers:
            try:
                self.subscribers[event_name].remove(callback)
            except ValueError:
                raise ValueError()

    def publish(self, event_name: str, *args, **kwargs) -> None:
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                callback(*args, **kwargs)
