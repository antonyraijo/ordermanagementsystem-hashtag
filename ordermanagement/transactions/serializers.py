from functools import reduce
from rest_framework import serializers

from transactions.models import Order, Product, PaymentTransactions


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class OrderCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        """Create and return order informations"""

        products = validated_data['products']
        payable_amount = reduce(lambda a,b:a+b, map(lambda x:x.price, products))    # total amount findout for given products

        order = Order(
            user=validated_data['user'],
            total_payable_amount=payable_amount
        )
        order.save()
        order.products.set(products)

        return order
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.name
        response['products'] = ProductSerializer(instance.products.all(), many=True).data

        return response


class PaymentTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTransactions
        fields = "__all__"
    
    def create(self, validated_data):
        """Create and return payment transaction datas"""

        request = self.context['request']
        order = validated_data['order']

        # user permission checking 
        if request.user != order.user:
            raise serializers.ValidationError({'error': 'Permission denied'})
        
        current_instalment_amount = validated_data['current_instalment_amount']
        transactions = PaymentTransactions.objects.filter(order=order)  # previous transactions queryset of given order

        payed_amount = reduce(lambda a,b:a+b, map(lambda x:x.current_instalment_amount, list(transactions)), 0.0)   # find out total payed amount for given order

        balance_amount_to_pay = order.total_payable_amount - payed_amount

        if balance_amount_to_pay == 0:
            raise serializers.ValidationError({'error': 'Payement completed for this order'})
        if current_instalment_amount == balance_amount_to_pay:
            balance_amount = 0
        if current_instalment_amount < balance_amount_to_pay:
            balance_amount = balance_amount_to_pay - current_instalment_amount
        if current_instalment_amount > balance_amount_to_pay:
            msg = "Balance amount to be pay only {} rupees for this order".format(balance_amount_to_pay)
            raise serializers.ValidationError({'error': msg})
        
        transact = PaymentTransactions(
            order=order,
            current_instalment_amount=current_instalment_amount,
            balance_amount_to_pay=balance_amount
        )
        transact.save()

        return transact

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['total_payable_amount'] = instance.order.total_payable_amount
        response['payed_amount'] = instance.order.total_payable_amount - instance.balance_amount_to_pay

        return response