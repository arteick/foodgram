import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

from .models import Subscription

User = get_user_model()


class AvatarSerializer(serializers.ModelSerializer):
    """Возвращает только значение поля avatar"""
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)

    def validate(self, data):
        if data.get('avatar') in ("", None):
            raise serializers.ValidationError(
                code=status.HTTP_400_BAD_REQUEST
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Cериализатор для пользователей"""
    avatar = Base64ImageField(allow_null=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'avatar', 'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Subscription.objects.filter(
                user=user, subscriber=obj
            ).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователей на основе сериализатора
    библиотеки djoser
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'password'
        )

    def validate_username(self, value):
        """Проверка поля "username" на соответствие шаблону."""
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                {'username': 'Имя пользователя содержит запрещённые символы.'},
            )
        return value


class SubscriptionSerializer(serializers.ModelSerializer):
    """Cериализатор для подписок"""

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'subscriber')
        read_only_fields = ('user', 'subscriber')

    def validate(self, data):
        if self.context.get('request').user == self.context.get('user'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!',
            )
        return data
