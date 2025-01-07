import os

from car.entity.car_image import CarImage
from car.repository.car_image_repository import CarImageRepository


class CarImageRepositoryImpl(CarImageRepository):
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

    def create(self, car, image):
        print(f"current working directory: {os.getcwd()}")
        uploadDirectory = os.path.join('../../../nuxt/notes/ui/assets/images/uploadImages')
        if not os.path.exists(uploadDirectory):
            os.makedirs(uploadDirectory)

        imagePath = os.path.join(uploadDirectory, image.name)
        with open(imagePath, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

            destination.flush()
            os.fsync(destination.fileno())

        return CarImage.objects.create(car=car, image=image)

    def findByCar(self, car):
        return CarImage.objects.get(car=car)
