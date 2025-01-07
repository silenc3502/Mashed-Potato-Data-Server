from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status

from excel.service.excel_service_impl import ExcelServiceImpl


class ExcelController(viewsets.ViewSet):
    excelService = ExcelServiceImpl.getInstance()

    def requestCreateExcelInfo(self, request):
        isSuccess = self.excelService.createExcelToDatabase()

        return JsonResponse({"isSuccess": isSuccess}, status=status.HTTP_200_OK)

    def requestDatabaseToExcel(self, request):
        isSuccess = self.excelService.createDatabaseToExcel()

        return JsonResponse({"isSuccess": isSuccess}, status=status.HTTP_200_OK)
