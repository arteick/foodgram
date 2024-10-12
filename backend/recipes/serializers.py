from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag, RecipeTag)
from users.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Cериализатор для ингридиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeTagSerializer(serializers.PrimaryKeyRelatedField):
    def to_representation(self, obj):
        return TagSerializer(instance=obj).data


class IngredientInputSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeOutputSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)
    tags = RecipeTagSerializer(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return Favorite.objects.filter(
                user=user, recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_anonymous:
            return ShoppingCart.objects.filter(
                user=user, recipe=obj
            ).exists()
        return False

    def create(self, validated_data):
        return super().create(validated_data)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Основной сериализатор для рецептов.
    Содержит все поля, кроме 'pub_date'.
    """
    author = UserSerializer(read_only=True)
    ingredients = IngredientInputSerializer(many=True)
    tags = RecipeTagSerializer(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            ingredient_obj = get_object_or_404(
                Ingredient,
                pk=ingredient.pop('id')
            )
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_obj,
                amount=ingredient.pop('amount')
            )
        for tag in tags:
            RecipeTag.objects.create(
                recipe=recipe,
                tag=tag
            )
        return recipe

    def to_representation(self, instance):
        return RecipeOutputSerializer(
            instance, context={'request': self.context.get('request')}
        ).data


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


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов с ограниченным набором полей"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
