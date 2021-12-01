from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from functools import reduce

from transactions.models import Order, PaymentTransactions

# admin site customisations
class CustomUserAdmin(UserAdmin):

    model = get_user_model()

    #custom methods to get order data along with user
    def number_of_orders(self, obj):
        return Order.objects.filter(user=obj).count()
    
    def total_amount(self, obj):
        orders = Order.objects.filter(user=obj)
        return reduce(lambda a,b:a+b, map(lambda x:x.total_payable_amount, list(orders)), 0.0)
    
    def total_payed_amount(self, obj):
        orders_id_list = Order.objects.filter(user=obj).values_list('id')
        transactions = PaymentTransactions.objects.filter(order__id__in=orders_id_list)
        return reduce(lambda a,b:a+b, map(lambda x:x.current_instalment_amount, list(transactions)), 0.0)
    
    def total_pending_amount(self, obj):
        total_amount = self.total_amount(obj)
        total_payed_amount = self.total_payed_amount(obj)
        return total_amount-total_payed_amount


    list_display = ("name", "email", "is_consumer", "number_of_orders", "total_amount", "total_payed_amount", "total_pending_amount")
    list_filter = ("is_consumer", "is_superuser", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("name", "email", "date_joined", "password")}),
        ("Permissions", {"fields": ("is_consumer", "is_superuser", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                    "is_consumer",
                    "date_joined",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(get_user_model(), CustomUserAdmin)

admin.site.site_header = "Order Management"
admin.site.site_title = "Order Management Portal"
admin.site.index_title = "Welcome To Order Management Portal"