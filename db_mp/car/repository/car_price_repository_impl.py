from car.entity.car_price import CarPrice
from car.repository.car_price_repository import CarPriceRepository


class CarPriceRepositoryImpl(CarPriceRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self, car, price):
        return CarPrice.objects.create(car=car, price=price)

    def findByCar(self, car):
        return CarPrice.objects.get(car=car)
