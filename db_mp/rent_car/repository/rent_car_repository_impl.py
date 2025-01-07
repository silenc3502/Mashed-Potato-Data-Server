from rent_car.entity.rent_car import RentCar
from rent_car.repository.rent_car_repository import RentCarRepository
from django.core.exceptions import ValidationError

class RentCarRepositoryImpl(RentCarRepository):
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
    
    def save(self, rent_car):
        try:
            if isinstance(rent_car, RentCar):
                rent_car.full_clean()  # Validate model fields
                rent_car.save()
            else:
                raise ValueError("rent_car must be an instance of the RentCar model.")
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}")

    def get_all(self):
        return list(RentCar.objects.all().values("name", "car_type", "price_per_day", "availability"))
