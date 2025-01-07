from django.urls import path, include
from rest_framework.routers import DefaultRouter

from car.controller.car_controller import CarController

router = DefaultRouter()
router.register(r"car", CarController, basename='car')

urlpatterns = [
    path('', include(router.urls)),
    path('list',
         CarController.as_view({ 'get': 'requestCarList' }),
         name='자동차 항목 요청'),
    path('create',
         CarController.as_view({ 'post': 'requestCarCreate' }),
         name='자동차 등록 요청'),
    path('read/<int:pk>',
         CarController.as_view({ 'get': 'requestCarRead' }),
         name='자동차 읽기 요청'),
]