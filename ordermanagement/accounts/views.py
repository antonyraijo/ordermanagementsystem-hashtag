from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class ConsumerCreationView(ModelViewSet):

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ['post']    # restricted to POST request


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            raise ValidationError({'error': 'Error! Please contact the support team'})
        return Response({
            'token': token.key,
            'id': user.id,
            'name': user.name,
            'email': user.email
        })