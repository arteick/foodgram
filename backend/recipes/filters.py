from django_filters.filters import BooleanFilter, CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from recipes.models import Recipe, Ingredient


class RecipeFilter(FilterSet):
    """<Необходимо заполнить>"""

    is_favorited = BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = BooleanFilter(field_name='is_in_shopping_cart')
    author = NumberFilter(field_name='author__id')
    tags = CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')


class IngridientFilter(FilterSet):
    """Фильтр по частичному вхождению в начале названия ингредиента('name')"""
    name = CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']
