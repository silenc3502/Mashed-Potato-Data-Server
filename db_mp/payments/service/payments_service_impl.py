from account.entity.account import Account
from account.repository.account_repository_impl import AccountRepositoryImpl
from payments.entity.payments import Payments
from payments.repository.payments_repository_impl import PaymentsRepositoryImpl
from payments.service.payments_service import PaymentsService


class PaymentsServiceImpl(PaymentsService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__paymentsRepository = PaymentsRepositoryImpl.getInstance()
            cls.__instance.__accountRepository = AccountRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def process(self, accountId, paymentKey, orderId, amount):
        try:
            print(f"accountId: {accountId}")
            account = self.__accountRepository.findById(accountId)

            paymentRequestData = {
                "paymentKey": paymentKey,
                "orderId": orderId,
                "amount": amount,
            }
            print(f"paymentRequestData: {paymentRequestData}")

            # 결제 요청을 레포지토리로 넘기고 결과 받기
            paymentResult = self.__paymentsRepository.request(paymentRequestData)
            print(f"paymentResult: {paymentResult}")

            if paymentResult:
                # 결제 정보를 DB에 저장
                payment = Payments(
                    account=account,
                    payment_key=paymentKey,
                    order_id=orderId,
                    amount=amount,
                    provider=paymentResult.get('easyPay', {}).get('provider'),
                    method=paymentResult.get('method'),
                    paid_at=paymentResult.get('approvedAt'),
                    receipt_url=paymentResult.get('receipt', {}).get('url'),
                )
                self.__paymentsRepository.create(payment)  # 결제 정보 DB에 저장

                return paymentResult
            else:
                raise Exception("결제 요청 처리 실패")

        except Exception as e:
            print(f"결제 처리 중 오류 발생: {e}")
            return {"error": "Internal server error", "success": False}, 500
