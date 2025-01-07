from excel.entity.excel_employee import ExcelEmployee
from excel.repository.excel_repository import ExcelRepository


class ExcelRepositoryImpl(ExcelRepository):
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

    def createMany(self, excelDictionary):
        employeeDictionary = [
            ExcelEmployee(
                name=excelElement['Name'],
                age=excelElement['Age'],
                city=excelElement['City'],
                score=excelElement['Score'],
                department=excelElement['Department']
            )
            for excelElement in excelDictionary
        ]

        ExcelEmployee.objects.bulk_create(employeeDictionary)

    def list(self):
        return ExcelEmployee.objects.all()
    