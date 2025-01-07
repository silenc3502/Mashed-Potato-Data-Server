from abc import ABC, abstractmethod


class ExcelRepository(ABC):

    @abstractmethod
    def createMany(self, excelDictionary):
        pass

    @abstractmethod
    def list(self):
        pass
