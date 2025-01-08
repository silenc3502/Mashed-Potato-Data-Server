from abc import ABC, abstractmethod


class BoardRepository(ABC):

    @abstractmethod
    def list(self, page, perPage):
        pass

    @abstractmethod
    def save(self, board):
        pass

    @abstractmethod
    def findById(self, boardId):
        pass

    @abstractmethod
    def deleteById(self, boardId):
        pass
