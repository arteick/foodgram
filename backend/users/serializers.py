import re

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

import recipes.serializers
from recipes.models import Recipe
from users.models import Subscription

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
                user=user, following=obj
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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ('user', 'following')
        read_only_fields = ('user', 'following')

    def validate(self, data):
        user = self.context.get('request').user
        following = self.context.get('following')
        if user == following:
            raise serializers.ValidationError(
                {'following: ''Нельзя подписаться на самого себя!'},
            )
        if Subscription.objects.filter(
            user=user, following=following
        ).exists():
            raise serializers.ValidationError(
                {'following': 'Вы уже подписаны на данного пользователя'},
            )
        return data

    def to_representation(self, instance):
        return SubscriptionOutputSerializer(
            instance.following,
            context=self.context
        ).data


class SubscriptionOutputSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода подписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'avatar', 'email', 'username', 'first_name',
                  'last_name', 'recipes', 'recipes_count', 'is_subscribed')

    def get_recipes(self, obj):
        limit = self.context.get('request').GET.get('recipes_limit')
        if not limit:
            self.context.get('request').POST.get('recipes_limit')
        recipes_query = obj.recipes.all()
        if limit:
            recipes_query = recipes_query[:int(limit)]
        return recipes.serializers.RecipeShortSerializer(
            recipes_query, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(
            author=obj.id
        ).count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Subscription.objects.filter(
                user=user, following=obj
            ).exists()
        return False
