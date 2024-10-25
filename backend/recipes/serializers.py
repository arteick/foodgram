from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Tag)
from rest_framework import serializers
from users.serializers import UserSerializer


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
    """
    Сериализатор для добавления тэгов в рецепт по pk
    и выводу полного содержимого объекта тэга
    """
    def to_representation(self, obj):
        return TagSerializer(instance=obj).data


class InputIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления игридиента в рецепт"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class OutputIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода ингридиентов в рецепте"""
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецетов.
    """
    author = UserSerializer(read_only=True)
    ingredients = InputIngredientSerializer(many=True)
    tags = RecipeTagSerializer(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def add_tags_and_ingredients(self, tags, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient.pop('id'),
                amount=ingredient.pop('amount')
            )
        for tag in tags:
            RecipeTag.objects.create(
                recipe=recipe,
                tag=tag
            )

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise serializers.ValidationError(
                'Добавьте теги'
            )
        tag_list = []
        for tag in tags:
            if tag in tag_list:
                raise serializers.ValidationError(
                    'Теги не могут повторяться'
                )
            tag_list.append(tag)
        return value

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise serializers.ValidationError(
                'Добавьте ингридиенты'
            )
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиенты не могут повторяться'
                )
            ingredients_list.append(ingredient)
        return value

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError(
                'Добавьте изображение для рецепта'
            )
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.add_tags_and_ingredients(
            tags, ingredients, recipe
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        self.add_tags_and_ingredients(
            tags, ingredients, instance
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return OutputRecipeSerializer(instance, context=self.context).data


class OutputRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода списка рецептов или отдельного рецепта.
    """
    author = UserSerializer()
    ingredients = OutputIngredientSerializer(
        many=True, source='ingredients_in_recipe'
    )
    tags = RecipeTagSerializer(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    is_favorited = serializers.ReadOnlyField(default=False)
    is_in_shopping_cart = serializers.ReadOnlyField(default=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Cериализатор для ибранного"""

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')
        read_only_fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe, context=self.context
        ).data

    def validate(self, data):
        if Favorite.objects.filter(
            user=self.context.get('request').user,
            recipe=self.context.get('recipe'),
        ).exists():
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в избранное'
            )
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины покупок"""

    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')
        read_only_fields = ('user', 'recipe')

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe, context=self.context
        ).data

    def validate(self, data):
        if ShoppingCart.objects.filter(
            user=self.context.get('request').user,
            recipe=self.context.get('recipe'),
        ).exists():
            raise serializers.ValidationError(
                'Вы уже добавили рецепт в корзину'
            )
        return data


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов с ограниченным набором полей"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
