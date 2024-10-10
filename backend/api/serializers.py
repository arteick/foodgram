import re

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer

from .models import (Favorite, Ingridient, Recipe, RecipeIngridient,
                     ShoppingCart, Subscription, Tag)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Cериализатор для пользователей"""
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'avatar',
        )

    def validate_username(self, value):
        """Проверка поля "username" на соответствие шаблону."""
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Имя пользователя содержит запрещённые символы.'
            )
        return value


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания пользователей на основе сериализатора
    библиотеки djoser
    """

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'password',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Cериализатор для подписок"""

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'subscriber')
        read_only_fields = ('user', 'subscriber')


class FavoriteSerializer(serializers.ModelSerializer):
    """Cериализатор для 'ибранного'"""

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')
        read_only_fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины покупок"""

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')
        read_only_fields = ('user', 'recipe')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngridientSerializer(serializers.ModelSerializer):
    """Cериализатор для ингридиентов"""

    class Meta:
        model = Ingridient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngridientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели RecipeIngridient, необходимой для связи N:M
    в моедил Recipe.
    """

    class Meta:
        model = RecipeIngridient
        fields = ('id', 'ingridient', 'recipe', 'amount')
        read_only_fields = ('recipe', 'ingridient')

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return super().to_representation(instance)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор для рецептов.
    Содержит все поля, кроме 'pub_date'.
    """
    author = UserSerializer(read_only=True)
    ingridients = RecipeIngridientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def create(self, validated_data):
        ingridients = validated_data.pop('ingridients')
        recipe = Recipe.objects.create(**validated_data)
        for ingridient in ingridients:
            id = ingridient.get('id')
            ingridient_obj = get_object_or_404(
                Ingridient,
                id=id
            )
            RecipeIngridient.objects.create(
                ingridient=ingridient_obj,
                **ingridient
            )

        return recipe


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов с ограниченным набором полей"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
