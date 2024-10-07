import base64
import re

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers, response

from .models import Cart
from .models import (Favorite, Ingridient, Recipe, RecipeIngridient,
                     Subscription, Tag)
from drf_base64.fields import Base64ImageField
from django.shortcuts import get_object_or_404

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'avatar',
        )

    def validate_username_pattern(self, value):
        """Проверка поля "username" на соответствие шаблону."""
        pattern = r'^[\w.@+-]+\Z'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Имя пользователя содержит запрещённые символы.'
            )
        return value


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('user', 'subscriber')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngridientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingridient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingridients = IngridientSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)
