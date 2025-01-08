from orders.entity.orders_items import OrdersItems
from orders.repository.order_item_repository import OrderItemRepository


class OrderItemRepositoryImpl(OrderItemRepository):
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

    def bulkCreate(self, orderItemList):
        for orderItem in orderItemList:
            print(f"bulkCreate() orderItem: {orderItem}")
            if not orderItem.orders:
                raise Exception(f"Order item with ID {orderItem.id} has no associated order.")
            print(
                f"Order ID: {orderItem.orders.id}, Car: {orderItem.car.id}, Quantity: {orderItem.quantity}, Price: {orderItem.price}")

        OrdersItems.objects.bulk_create(orderItemList)
