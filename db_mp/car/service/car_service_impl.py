from django.db import transaction

from car.repository.car_description_repository_impl import CarDescriptionRepositoryImpl
from car.repository.car_image_repository_impl import CarImageRepositoryImpl
from car.repository.car_price_repository_impl import CarPriceRepositoryImpl
from car.repository.car_repository_impl import CarRepositoryImpl
from car.service.car_service import CarService


class CarServiceImpl(CarService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__carRepository = CarRepositoryImpl.getInstance()
            cls.__instance.__carPriceRepository = CarPriceRepositoryImpl.getInstance()
            cls.__instance.__carDescriptionRepository = CarDescriptionRepositoryImpl.getInstance()
            cls.__instance.__carImageRepository = CarImageRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def requestList(self, page, perPage):
        return self.__carRepository.list(page, perPage)

    def createCar(self, title, price, description, image):
        with transaction.atomic():
            savedCar = self.__carRepository.create(title)
            self.__carPriceRepository.create(savedCar, price)
            self.__carDescriptionRepository.create(savedCar, description)
            self.__carImageRepository.create(savedCar, image)

    def readCar(self, id):
        with transaction.atomic():
            foundCar = self.__carRepository.findById(id)
            print(f"foundCar: {foundCar}")
            foundCarPrice = self.__carPriceRepository.findByCar(foundCar)
            print(f"foundCarPrice: {foundCarPrice}")
            foundCarImage = self.__carImageRepository.findByCar(foundCar)
            print(f"foundCarImage: {foundCarImage}")
            foundCarDescription = self.__carDescriptionRepository.findByCar(foundCar)
            print(f"foundCarDescription: {foundCarDescription}")

            readCar = {
                'id': foundCar.getId(),
                'title': foundCar.getTitle(),
                'price': foundCarPrice.getPrice(),
                'image': foundCarImage.getImage(),
                'description': foundCarDescription.getDescription()
            }

            return readCar
