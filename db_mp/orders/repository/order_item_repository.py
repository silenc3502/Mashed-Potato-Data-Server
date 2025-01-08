from abc import ABC, abstractmethod


class OrderItemRepository(ABC):

    @abstractmethod
    def bulkCreate(self, orderItemList):
        pass