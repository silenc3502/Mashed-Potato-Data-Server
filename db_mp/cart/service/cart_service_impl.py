from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from account.repository.account_repository_impl import AccountRepositoryImpl
from cart.entity.cart import Cart
from cart.repository.cart_repository_impl import CartRepositoryImpl
from cart.service.cart_service import CartService
from game_software.entity.game_software import GameSoftware
from game_software.entity.game_software_image import GameSoftwareImage
from game_software.entity.game_software_price import GameSoftwarePrice
from game_software.repository.game_software_repository_impl import GameSoftwareRepositoryImpl


class CartServiceImpl(CartService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__cartRepository = CartRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()
            cls.__instance.__gameSoftwareRepository = GameSoftwareRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def createCart(self, accountId, cart):
        foundAccount = self.__accountRepository.findById(accountId)

        if not foundAccount:
            raise Exception("해당 accountId에 해당하는 account를 찾을 수 없습니다.")

        foundGameSoftware = self.__gameSoftwareRepository.findById(cart["id"])

        if not foundGameSoftware:
            raise Exception("해당 gameSoftwareId에 해당하는 게임을 찾을 수 없습니다.")

        foundCart = self.__cartRepository.findCartByAccountAndGameSoftware(foundAccount, foundGameSoftware)

        if foundCart:
            foundCart.quantity += cart["quantity"]
            updatedCart = self.__cartRepository.save(foundCart)
            return updatedCart

        newCart = Cart(
            account=foundAccount,
            gameSoftware=foundGameSoftware,
            quantity=cart["quantity"]
        )
        savedCart = self.__cartRepository.save(newCart)
        return savedCart

    def listCart(self, accountId, page, pageSize):
        try:
            print(f"listCart() pageSize: {pageSize}")

            # Account 확인
            account = self.__accountRepository.findById(accountId)
            if not account:
                raise ValueError(f"Account with ID {accountId} not found.")
            print(f"Account found: {account}")

            # Cart 목록 가져오기 (페이지네이션 적용된 결과)
            paginatedCartList = self.__cartRepository.findCartByAccount(account, page, pageSize)
            print(f"Paginated cart list query: {paginatedCartList}")

            # 전체 아이템 수 계산
            total_items = paginatedCartList.paginator.count  # Paginator에서 count 값을 사용

            # 필요한 데이터만 추출
            cartDataList = [
                {
                    "id": cart.id,
                    "title": cart.gameSoftware.title,
                    "price": cart.price,
                    "image": cart.image,
                    "quantity": cart.quantity,
                }
                for cart in paginatedCartList
            ]

            print(f"Total items: {total_items}")
            print(f"Page items: {len(cartDataList)}")

            return cartDataList, total_items  # total_items를 반환

        except Exception as e:
            print(f"Unexpected error in listCart: {e}")
            raise

    def removeCart(self, accountId, cartId):
        try:
            cart = self.__cartRepository.findById(cartId)
            print(f"cart: {cart}")
            if cart is None or str(cart.account.id) != str(accountId):
                return {
                    "error": "해당 카트를 찾을 수 없거나 소유자가 일치하지 않습니다.",
                    "success": False
                }

            result = self.__cartRepository.deleteById(cartId)
            if result:
                return {
                    "success": True,
                    "message": "카트 항목이 삭제되었습니다."
                }

        except Exception as e:
            print(f"Error in CartService.removeCart: {e}")
            return {
                "error": "서버 내부 오류",
                "success": False
            }
    