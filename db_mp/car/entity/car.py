from django.db import models

class Car(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'car'
        app_label = 'car'

    def __str__(self):
        return f"Car(id={self.id}, title={self.title})"

    def getId(self):
        return self.id

    def getTitle(self):
        return self.title

    def getCategory(self):
        return self.category
