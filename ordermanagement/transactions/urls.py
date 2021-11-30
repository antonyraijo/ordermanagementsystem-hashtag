from django.urls import path, include
from rest_framework.routers import SimpleRouter

from transactions.views import OrderCreationView, PaymentTransactionView

router = SimpleRouter()

router.register('order-creation', OrderCreationView)
router.register('payment-transaction', PaymentTransactionView)
urlpatterns = [
        path('', include(router.urls)),
] + router.urls