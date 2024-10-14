from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS

from utils.mixins import CustomUpdateModelMixin
from .pagination import RecipePageNumberLimit

from .filters import IngridientFilter, RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          CreateRecipeSerializer, OutputRecipeSerializer,
                          RecipeShortSerializer, ShoppingCartSerializer,
                          TagSerializer)
from rest_framework.decorators import action

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


class RecipeViewSet(mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Рецепты: CRUD"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    pagination_class = RecipePageNumberLimit
    http_method_names = ['patch', 'get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OutputRecipeSerializer
        return CreateRecipeSerializer


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
