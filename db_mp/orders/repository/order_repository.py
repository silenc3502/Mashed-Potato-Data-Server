from abc import ABC, abstractmethod


class OrderRepository(ABC):

    @abstractmethod
    def save(self, orders):
        pass

    @abstractmethod
    def findById(self, orderId):
        pass
