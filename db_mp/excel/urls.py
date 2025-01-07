from django.urls import path, include
from rest_framework.routers import DefaultRouter

from excel.controller.excel_controller import ExcelController

router = DefaultRouter()
router.register(r"excel", ExcelController, basename='excel')

urlpatterns = [
    path('', include(router.urls)),
    path('request-create-excel2db',
         ExcelController.as_view({ 'get': 'requestCreateExcelInfo' }),
         name='excel 정보 데이터 생성'),
    path('request-create-db2excel',
         ExcelController.as_view({ 'get': 'requestDatabaseToExcel' }),
         name='DB 데이터를 excel로 생성'),
]