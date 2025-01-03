from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rent_car.controller.rent_car_controller import RentCarController

router = DefaultRouter()
router.register(r"rent_car", RentCarController, basename='rent_car')

urlpatterns = [
    path('', include(router.urls)),
#    path('create-car',
#         RentCarController.as_view({ 'post': 'create_car' }),
#         name='렌트카 정보 생성'),
    path('get-cars',
         RentCarController.as_view({ 'get': 'get_cars' }),
         name='렌트카 정보 리스트 획득'),
]