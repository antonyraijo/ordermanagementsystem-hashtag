from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsConsumer
from transactions.models import Order, PaymentTransactions
from transactions.serializers import OrderCreationSerializer, PaymentTransactionSerializer


class OrderCreationView(ModelViewSet):
    permission_classes = [IsConsumer]   # only permited for 'consumer' type users
    serializer_class = OrderCreationSerializer
    queryset = Order.objects.all()
    http_method_names = ['post']    # restricted to POST request


class PaymentTransactionView(ModelViewSet):
    permission_classes = [IsConsumer]   # only permited for 'consumer' type users
    serializer_class = PaymentTransactionSerializer
    queryset = PaymentTransactions.objects.all()
    http_method_names = ['post']    # restricted to POST request