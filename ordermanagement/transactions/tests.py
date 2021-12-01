from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts.models import CustomUser
from transactions.models import Product, Order

ADMIN_CREDENTIALS = {'username': 'admin@mail.com', 'password': 'admin_password'}
USER1_CREDENTIALS = {'username': 'user@mail.com', 'password': 'user_password'}
USER2_CREDENTIALS = {'username': 'user2@mail.com', 'password': 'user2_password'}


class OrderCreationViewTestCase(APITestCase):

    def setUp(self):

        CustomUser.objects.create_superuser(email='admin@mail.com', password='admin_password')
        self.user1 = CustomUser.objects.create_user(email='user@mail.com', password='user_password')
        self.user1.is_consumer = True
        self.user1.save()
        self.token1 = Token.objects.get_or_create(user=self.user1)

        self.user2 = CustomUser.objects.create_user(email='user2@mail.com', password='user2_password')
        self.token2 = Token.objects.get_or_create(user=self.user2)

        self.product1 = Product.objects.create(name="p1", price=10.50)
        self.product2 = Product.objects.create(name="p2", price=100)
        self.product3 = Product.objects.create(name="p3", price=55.99)


    def test_order_creation(self):
        self.client.login(**USER1_CREDENTIALS)
        self.client.login(**ADMIN_CREDENTIALS)
        payload = {
            'user': self.user1.pk,
            'products': [self.product1.id, self.product2.id]
        }

        auth = 'Token {}'.format(self.token1[0])
        response = self.client.post(
            '/transact/order-creation/',
            data=payload,
            HTTP_AUTHORIZATION=auth, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_payable_amount'], 110.5)
        self.assertEqual(len(response.data['products']), 2)

    
    def test_order_creation_not_consumer(self):
        self.client.login(**USER2_CREDENTIALS)
        self.client.login(**ADMIN_CREDENTIALS)
        payload = {
            'user': self.user2.pk,
            'products': [self.product1.id, self.product2.id]
        }

        auth = 'Token {}'.format(self.token2[0])
        response = self.client.post(
            '/transact/order-creation/',
            data=payload,
            HTTP_AUTHORIZATION=auth, 
            format='json'
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TransactionCreationViewTestCase(APITestCase):

    def setUp(self):

        CustomUser.objects.create_superuser(email='admin@mail.com', password='admin_password')
        self.user1 = CustomUser.objects.create_user(email='user@mail.com', password='user_password')
        self.user1.is_consumer = True
        self.user1.save()
        self.token1 = Token.objects.get_or_create(user=self.user1)

        self.user2 = CustomUser.objects.create_user(email='user2@mail.com', password='user2_password')
        self.token2 = Token.objects.get_or_create(user=self.user2)

        self.product1 = Product.objects.create(name="p1", price=10.50)
        self.product2 = Product.objects.create(name="p2", price=100)
        self.product3 = Product.objects.create(name="p3", price=55.99)

        self.order1 = Order.objects.create(
            user=self.user1.pk,
            products=[self.product1.pk, self.product2.pk],
            total_payable_amount=110.5
        )
