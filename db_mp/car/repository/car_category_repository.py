from abc import ABC, abstractmethod


class CarCategoryRepository(ABC):

    @abstractmethod
    def create(self, car, category):
        pass

    @abstractmethod
    def findByCar(self, car):
        pass
