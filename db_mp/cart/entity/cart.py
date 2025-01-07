from django.db import models

from account.entity.account import Account
from car.entity.car import Car

# GameSoftware을 Car로 바꿔야함

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="carts")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="carts")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart'
        app_label = 'cart'

    def __str__(self):
        return f"Cart(id={self.id}, account={self.account}, car={self.car})"

    def getId(self):
        return self.id

    def getAccount(self):
        return self.account

    def getCar(self):
        return self.car
