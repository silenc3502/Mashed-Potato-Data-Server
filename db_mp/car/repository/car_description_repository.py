from abc import ABC, abstractmethod


class CarDescriptionRepository(ABC):

    @abstractmethod
    def create(self, car, description):
        pass

    @abstractmethod
    def findByCar(self, car):
        pass
