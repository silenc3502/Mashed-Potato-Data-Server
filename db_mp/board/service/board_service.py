from abc import ABC, abstractmethod


class BoardService(ABC):

    @abstractmethod
    def requestList(self, page, perPage):
        pass

    @abstractmethod
    def requestCreate(self, title, content, accountId):
        pass

    @abstractmethod
    def requestRead(self, boardId):
        pass

    @abstractmethod
    def requestDelete(self, boardId, accountId):
        pass
