from django_filters.filters import (CharFilter, ModelMultipleChoiceFilter,
                                    NumberFilter)
from django_filters.rest_framework import FilterSet
from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр для рецптов"""

    is_in_shopping_cart = NumberFilter(
        field_name='is_in_shopping_cart')
    is_favorited = NumberFilter(
        field_name='is_in_shopping_cart')
    author = NumberFilter(field_name='author__id')
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')


class IngridientFilter(FilterSet):
    """Фильтр по частичному вхождению в начале названия ингредиента('name')"""
    name = CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']
