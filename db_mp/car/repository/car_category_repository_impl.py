from car.entity.car_category import CarCategory
from car.repository.car_category_repository import CarCategoryRepository


class CarCategoryRepositoryImpl(CarCategoryRepository):
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

    def create(self, car, category):
        return CarCategory.objects.create(car=car, category=category)

    def findByCar(self, car):
        return CarCategory.objects.get(car=car)
