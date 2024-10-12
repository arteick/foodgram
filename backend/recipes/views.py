from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from .filters import RecipeFilter, IngridientFilter
from utils.mixins import CustomUpdateModelMixin
from utils.pagination import PageNumberAndLimit

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipeIngredient
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          ShoppingCartSerializer, TagSerializer)

User = get_user_model()


class CartViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Корзина: POST, DELETE"""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    lookup_field = 'recipe_id'

    def get_recipe(self):
        return get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = RecipeShortSerializer(instance=self.get_recipe())
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe()
        )

    def perform_destroy(self, instance):
        instance = get_object_or_404(
            ShoppingCart,
            user=self.request.user,
            recipe=self.get_recipe()
        )
        instance.delete()


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Избранное: POST, DELETE"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe_id'

    def get_recipe(self):
        return get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = RecipeShortSerializer(instance=self.get_recipe())
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe()
        )

    def perform_destroy(self, instance):
        instance = get_object_or_404(
            Favorite,
            user=self.request.user,
            recipe=self.get_recipe()
        )
        instance.delete()


class RecipeViewSet(CustomUpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Рецепты: CRUD"""
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги: CRUD только для администратора"""
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ингридиенты: CRUD только для администратора"""
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngridientFilter
