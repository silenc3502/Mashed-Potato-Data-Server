from abc import ABC, abstractmethod


class RentCarService(ABC):

    @abstractmethod
    def add_car(self, name, car_type, price_per_day, availability):
        pass

    @abstractmethod
    def list_cars(self):
        pass