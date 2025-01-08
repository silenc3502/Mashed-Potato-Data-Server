from django.db import models

from car.entity.car import Car
from orders.entity.orders import Orders


class OrdersItems(models.Model):
    id = models.AutoField(primary_key=True)
    orders = models.ForeignKey(Orders, related_name="items", on_delete=models.CASCADE)  # Order와 연결
    car = models.ForeignKey(Car, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item: {self.quantity} x {self.price}"

    class Meta:
        db_table = 'orders_items'
        app_label = 'orders'