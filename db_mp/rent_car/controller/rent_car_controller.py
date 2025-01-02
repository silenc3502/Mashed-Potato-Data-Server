from rest_framework.response import Response
from rest_framework import viewsets, status

from rent_car.serializer.rent_car_serializer import RentCarSerializer
from rent_car.service.rent_car_service_impl import RentCarServiceImpl


class RentCarController(viewsets.ViewSet):
    __carService = RentCarServiceImpl.getInstance()

    def __init__(self):
        super().__init__()
        self.__carService = RentCarServiceImpl.getInstance()

    def create_car(self, request):
        print("Request Headers:", request.headers)  # 헤더 디버깅
        print("Raw Request Body:", request.body)  # 요청 본문 디버깅
        print("Parsed Request Data:", request.data)  # 파싱된 데이터 디버깅

        serializer = RentCarSerializer(data=request.data)
        if serializer.is_valid():
            try:
                self.__carService.add_car(**serializer.validated_data)
                return Response({"message": "Car created successfully"}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        print("Serializer Errors:", serializer.errors)  # Serializer 오류 출력
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_cars(self, request):
        cars = self.__carService.list_cars()
        unique_cars = {car['name']: car for car in cars}.values()  # 중복 제거 (name 기준)
        return Response({"cars": list(unique_cars)}, status=status.HTTP_200_OK)
