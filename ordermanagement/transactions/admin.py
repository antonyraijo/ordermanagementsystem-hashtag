from django.contrib import admin

from transactions.models import Product, Order, PaymentTransactions


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(PaymentTransactions)
