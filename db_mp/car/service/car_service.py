from abc import ABC, abstractmethod


class CarService(ABC):

    @abstractmethod
    def requestList(self, page, perPage):
        pass

    @abstractmethod
    def createCar(self, title, price, description, image):
        pass

    @abstractmethod
    def readCar(self, id):
        pass
