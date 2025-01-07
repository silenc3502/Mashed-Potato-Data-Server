from abc import ABC, abstractmethod


class CarImageRepository(ABC):

    @abstractmethod
    def create(self, car, image):
        pass

    @abstractmethod
    def findByCar(self, car):
        pass
    