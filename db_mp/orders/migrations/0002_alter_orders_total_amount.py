# Generated by Django 5.1.4 on 2025-01-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
