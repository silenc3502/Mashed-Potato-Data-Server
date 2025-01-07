import os.path
import pandas as pd

from excel.repository.excel_repository_impl import ExcelRepositoryImpl
from excel.service.excel_service import ExcelService


class ExcelServiceImpl(ExcelService):
    __instance = None

    __fixedExcelFile = "fixedExcelForTest.xlsx"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__excelRepository = ExcelRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def __readExcel(self, excelFilePath):
        try:
            dataFrame = pd.read_excel(excelFilePath)
            excelDataDictionary = dataFrame.to_dict(orient='records')
            return excelDataDictionary

        except Exception as e:
            print(f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")
            return []

    def createExcelToDatabase(self):
        currentWorkingDirectory = os.getcwd()
        excelFilePath = os.path.join(currentWorkingDirectory, "resource", self.__fixedExcelFile)

        readExcelData = self.__readExcel(excelFilePath)
        print(f"readExcelData: {readExcelData}")

        self.__excelRepository.createMany(readExcelData)
        return True

    def createDatabaseToExcel(self):
        currentWorkingDirectory = os.getcwd()
        generateExcelPath = os.path.join(currentWorkingDirectory, "generate", "excel_test.xlsx")

        excelDataList = self.__excelRepository.list()
        print(f"excelDataList: {excelDataList}")
        employeeDictionary = excelDataList.values("name", "age", "city", "score", "department")

        dataFrame = pd.DataFrame(employeeDictionary)
        dataFrame.to_excel(generateExcelPath, index=False, engine='openpyxl')
        return True
