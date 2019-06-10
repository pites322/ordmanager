from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Staff(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=80, verbose_name="Фамилия")
    first_name = models.CharField(max_length=80, verbose_name="Имя")
    second_name = models.CharField(max_length=80, verbose_name="Отчество", null=True, blank=True)

    def __str__(self):
        full_name = str(self.surname) + ' ' + str(self.first_name) + ' ' + str(self.second_name)
        return full_name


class Orders(models.Model):
    ADD_TO_BASKET = 0
    CONFIRMED = 1
    READY = 2

    BUY_STRATUS = (
        (ADD_TO_BASKET, 'Доб.'),
        (CONFIRMED, "Подтв."),
        (READY, "Гот.")
    )

    buyer = models.ForeignKey(Staff, on_delete=models.CASCADE)
    buyId = models.CharField(max_length=80)
    name_of_buy = models.CharField(max_length=80)
    amount = models.IntegerField(default=1)
    price_of_buy = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    data_of_buy = models.DateField(auto_now=True)
    status = models.PositiveSmallIntegerField(null=True, choices=BUY_STRATUS, default=ADD_TO_BASKET)