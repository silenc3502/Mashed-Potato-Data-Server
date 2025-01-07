from abc import ABC, abstractmethod

class RentCarRepository(ABC):
    @abstractmethod
    def save(self, car):
        pass

    @abstractmethod
    def get_all(self):
        pass
