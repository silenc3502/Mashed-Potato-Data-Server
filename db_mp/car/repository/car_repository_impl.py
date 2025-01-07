from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from car.entity.car import Car
from car.entity.car_image import CarImage
from car.entity.car_price import CarPrice
from car.repository.car_repository import CarRepository


class CarRepositoryImpl(CarRepository):
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

    def list(self, page=1, perPage=8):
        priceSubQuery = CarPrice.objects.filter(car=OuterRef('pk')).values('price')[:1]
        imageSubQuery = CarImage.objects.filter(car=OuterRef('pk')).values('image')[:1]

        carList = Car.objects.annotate(
            price=Coalesce(Subquery(priceSubQuery), Value(0)),
            image=Coalesce(Subquery(imageSubQuery), Value('')),
        )

        paginator = Paginator(carList, perPage)

        try:
            paiginatedCarDataList = paginator.page(page)
        except PageNotAnInteger:
            paiginatedCarDataList = paginator.page(1)
        except EmptyPage:
            paiginatedCarDataList = []

        paginatedCarList = [
            {
                'id': car.id,
                'title': car.title,
                'price': car.price,
                'image': car.image,
            }
            for car in paiginatedCarDataList
        ]

        print(f"Total items: {len(carList)}")
        print(f"Page items: {len(paginatedCarList)}")

        return paginatedCarList, paginator.num_pages

    def findAll(self):
        return Car.objects.all()

    def create(self, title):
        return Car.objects.create(title=title)

    def findById(self, id):
        return Car.objects.get(id=id)
