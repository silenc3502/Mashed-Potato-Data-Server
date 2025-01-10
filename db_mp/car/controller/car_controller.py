import uuid

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.status import HTTP_200_OK

from car.service.car_service_impl import CarServiceImpl
from redis_cache.service.redis_cache_service_impl import RedisCacheServiceImpl


class CarController(viewsets.ViewSet):
    carService = CarServiceImpl.getInstance()
    redisCacheService = RedisCacheServiceImpl.getInstance()

    def requestCarList(self, request):
        getRequest = request.GET
        page = int(getRequest.get("page", 1))
        perPage = int(getRequest.get("perPage", 8))
        paginatedCarList, totalPages = self.carService.requestList(page, perPage)

        return JsonResponse({
            "dataList": paginatedCarList,
            "totalPages": totalPages
        }, status=status.HTTP_200_OK)

    def requestCarCreate(self, request):
        postRequest = request.data

        carImage = request.FILES.get('carImage')
        carTitle = postRequest.get('carTitle')
        carPrice = postRequest.get('carPrice')
        carDescription = postRequest.get('carDescription')
        carCategory = postRequest.get('carCategory')
        print(f"carImage: {carImage}, "
              f"carTitle: {carTitle}, "
              f"carPrice: {carPrice}, "
              f"carDescription: {carDescription}, "
              f"carCategory: {carCategory}")

        if not all([carImage, carTitle, carPrice, carDescription, carCategory]):
            return JsonResponse({"error": '모든 내용을 채워주세요!'}, status=status.HTTP_400_BAD_REQUEST)

        savedCar = self.carService.createCar(
            carTitle,
            carPrice,
            carDescription,
            carImage,
            carCategory
        )

        return JsonResponse({"data": savedCar}, status=status.HTTP_200_OK)

    def requestCarRead(self, request, pk=None):
        try:
            if not pk:
                return JsonResponse({"error": "ID를 제공해야 합니다."}, status=400)

            print(f"requestCarRead() -> pk: {pk}")
            readCar = self.carService.readCar(pk)

            return JsonResponse(readCar, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
