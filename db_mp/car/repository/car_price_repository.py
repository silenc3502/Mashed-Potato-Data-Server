from abc import ABC, abstractmethod


class CarPriceRepository(ABC):

    @abstractmethod
    def create(self, car, price):
        pass

    @abstractmethod
    def findByCar(self, car):
        pass
