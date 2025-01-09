from django.db import models

from car.entity.car import Car


class CarCategory(models.Model):
    id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="categories")
    category = models.CharField(max_length=30, null=True)

    class Meta:
        db_table = 'car_category'
        app_label = 'car'

    def __str__(self):
        return f"CarCategory(id={self.id}, category={self.category})"

    def getCategory(self):
        return self.category
