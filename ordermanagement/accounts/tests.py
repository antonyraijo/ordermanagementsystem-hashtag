from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser

ADMIN_CREDENTIALS = {'username': 'admin@mail.com', 'password': 'admin_password'}


class ConsumerCreationViewTestCase(APITestCase):

    def setUp(self):
        self.admin = CustomUser.objects.create_superuser(email='admin@mail.com', password='admin_password')
        self.token = Token.objects.get_or_create(user=self.admin)

    def test_consumer_creation(self):
        self.client.login(**ADMIN_CREDENTIALS)
        payload = {
            'name': 'test1',
            'email': 'test1@mail.com',
            'password': 'password'
        }

        auth = 'Token {}'.format(self.token[0])

        response = self.client.post(
            '/auth/consumer-creation/',
            data=payload,
            HTTP_AUTHORIZATION=auth,
            format='json'
        )
        self.assertEqual(response.data['name'], 'test1')
        self.assertEqual(response.data['email'], 'test1@mail.com')
        self.assertEqual(response.data['is_consumer'], True)
