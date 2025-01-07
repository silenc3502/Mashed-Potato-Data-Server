from car.entity.car_description import CarDescription
from car.repository.car_description_repository import CarDescriptionRepository


class CarDescriptionRepositoryImpl(CarDescriptionRepository):
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

    def create(self, car, description):
        return CarDescription.objects.create(car=car, description=description)

    def findByCar(self, car):
        return CarDescription.objects.get(car=car)
