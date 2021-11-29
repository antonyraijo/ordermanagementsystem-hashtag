from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "is_consumer", "password"]

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""

        user = CustomUser(
            email = validated_data['email'],
            name = validated_data['name'],
            is_consumer = True
        )

        user.set_password(validated_data['password'])
        user.save()

        return user