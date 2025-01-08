from django.db import transaction

from account.repository.account_repository_impl import AccountRepositoryImpl
from cart.repository.cart_repository_impl import CartRepositoryImpl
from car.repository.car_price_repository_impl import CarPriceRepositoryImpl
from car.repository.car_repository_impl import CarRepositoryImpl

from orders.entity.orders import Orders
from orders.entity.orders_items import OrdersItems
from orders.entity.orders_status import OrdersStatus
from orders.repository.order_item_repository_impl import OrderItemRepositoryImpl
from orders.repository.order_repository_impl import OrderRepositoryImpl
from orders.service.order_service import OrderService


class OrderServiceImpl(OrderService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__cartRepository = CartRepositoryImpl.getInstance()
            cls.__instance.__orderRepository = OrderRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__orderItemRepository = OrderItemRepositoryImpl.getInstance()
            cls.__instance.__carRepository = CarRepositoryImpl.getInstance()
            cls.__instance.__carPriceRepository = CarPriceRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    @transaction.atomic
    def createOrder(self, accountId, items, total):
        account = self.__accountRepository.findById(accountId)

        if not account:
            raise Exception(f"Account id {accountId} 존재하지 않음.")

        # 2. 총 금액 검증
        if not isinstance(total, (int, float)) or total <= 0:
            raise Exception("유효하지 않은 총 금액입니다.")

        # 3. 주문 항목 검증
        if not items or not isinstance(items, list):
            raise Exception("유효하지 않은 주문 항목입니다.")

        orders = Orders(
            account=account,
            total_amount=total,
            status=OrdersStatus.PENDING,
        )
        orders = self.__orderRepository.save(orders)
        print(f"order 생성: {orders}")

        orderItemList = []

        for item in items:
            cartItem = self.__cartRepository.findById(item["id"])
            if not cartItem:
                raise Exception(f"Cart item ID {item['id']} 존재하지 않음.")

            car = cartItem.getCar()
            if not car:
                raise Exception(f"Car with ID {car.getId()} 존재하지 않음.")

            carPrice = self.__carPriceRepository.findByCar(car)

            orderItem = OrdersItems(
                orders=orders,  # orders가 올바르게 연결되었는지 확인
                car=car,
                quantity=item["quantity"],
                price=carPrice.getPrice() * item["quantity"],
            )
            orderItemList.append(orderItem)

        print(f"orderItemList: {orderItemList}")

        if orderItemList:
            self.__orderItemRepository.bulkCreate(orderItemList)

        return orders.getId()