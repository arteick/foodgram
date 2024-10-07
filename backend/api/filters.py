from django_filters.filters import BooleanFilter, CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from .models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter()
    is_in_shopping_cart = BooleanFilter()
    author = NumberFilter(field_name='author__id', lookup_expr='icontains')
    tags = CharFilter(field_name='tags__slug', lookup_expr='icontains')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')
