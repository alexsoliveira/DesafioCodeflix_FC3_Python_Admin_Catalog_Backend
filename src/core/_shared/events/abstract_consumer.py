from abc import ABC, abstractmethod


class AbstractConsumer(ABC):
    @abstractmethod
    def on_message(self, message):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass