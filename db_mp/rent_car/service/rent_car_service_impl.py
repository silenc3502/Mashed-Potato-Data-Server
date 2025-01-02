from rent_car.entity.rent_car import RentCar
from rent_car.repository.rent_car_repository_impl import RentCarRepositoryImpl
from rent_car.service.rent_car_service import RentCarService

class RentCarServiceImpl(RentCarService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__carRepository = RentCarRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def reset_instance(cls):
        cls.__instance = None

    def add_car(self, name, car_type, price_per_day, availability):
        if RentCar.objects.filter(name=name).exists():
            raise ValueError(f"A car with the name '{name}' already exists.")
        rent_car = RentCar(
            name=name,
            car_type=car_type,
            price_per_day=price_per_day,
            availability=availability
        )
        self.__carRepository.save(rent_car)

    def list_cars(self):
        cars = self.__carRepository.get_all()
        if not cars:
            print("No cars available in the database.")
            return []
        return cars
