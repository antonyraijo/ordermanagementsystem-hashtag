from django.db import models

from accounts.models import CustomUser


class Product(models.Model):

    name = models.CharField(max_length=64, unique=True)
    price = models.FloatField()

    def __str__(self):
        return "{}-{}".format(self.name, self.price)


class Order(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_orders')
    products = models.ManyToManyField(Product, related_name='choose_products')
    total_payable_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "orderID - " + str(self.pk)


class PaymentTransactions(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    current_instalment_amount = models.FloatField()
    balance_amount_to_pay = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Payment transactions'

    def __str__(self):
        return "transactionID - " + str(self.pk)
