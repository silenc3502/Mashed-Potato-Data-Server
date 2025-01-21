from django.core.exceptions import ObjectDoesNotExist

from account.entity.account import Account
from account.entity.account_role_type import AccountRoleType
from account.entity.role_type import RoleType
from account.repository.account_repository import AccountRepository


class AccountRepositoryImpl(AccountRepository):
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

    def save(self, email):
        print(f"email: {email}")
        defaultRoleType = AccountRoleType.objects.filter(role_type=RoleType.NORMAL).first()

        # 만약 기본 역할이 없다면, 새로 생성
        if not defaultRoleType:
            defaultRoleType = AccountRoleType(role_type=RoleType.NORMAL)
            defaultRoleType.save()
            print(f"Created new defaultRoleType: {defaultRoleType}")
        else:
            print(f"Found existing defaultRoleType: {defaultRoleType}")

        print(f"defaultRoleType: {defaultRoleType}")

        account = Account(email=email, role_type=defaultRoleType)
        print(f"account: {account}")

        account.save()
        return account

    def findById(self, accountId):
        try:
            return Account.objects.get(id=accountId)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(f"Account ID {accountId} 존재하지 않음.")

    def findByEmail(self, email):
        try:
            print(f"findByEmail -> email: {email}")
            account = Account.objects.get(email=email)
            print(f"findByEmail result: {account}")
            return account
        except Account.DoesNotExist:
            print(f"Account with email {email} does not exist.")
            raise ObjectDoesNotExist(f"Account {email} does not exist.")
        except Exception as e:
            print(f"Unexpected error in findByEmail: {e}")
            raise
