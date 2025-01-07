from abc import ABC, abstractmethod


class ExcelService(ABC):
    @abstractmethod
    def createExcelToDatabase(self):
        pass

    @abstractmethod
    def createDatabaseToExcel(self):
        pass
