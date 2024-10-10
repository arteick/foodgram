from django.contrib.auth import get_user_model
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .mixins import CustomUpdateModelMixin
from .models import (
    ShoppingCart, Favorite, Ingridient,
    Recipe, Subscription, Tag
)
from .pagination import PageNumberAndLimit
from .serializers import (ShoppingCartSerializer, FavoriteSerializer,
                          IngridientSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer, RecipeShortSerializer)

User = get_user_model()


class UserViewSet(CustomUpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Пользователи: CRUD."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberAndLimit

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['put', 'delete'],
        pagination_class=None,
        url_path='me/avatar',
        url_name='set_avatar'
    )
    def add_avatar(self, request):
        """Добавление изображения профиля."""
        if self.request.method == 'PUT':
            self.partial_update()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)

        return obj


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Подписки: POST, DELETE."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberAndLimit
    lookup_field = 'user_id'

    def get_user(self):
        return get_object_or_404(
            User, id=self.kwargs.get('user_id')
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = UserSerializer(instance=self.get_user())
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(
            subscriber=self.request.user,
            user=self.get_user()
        )

    def perform_destroy(self, instance):
        instance = get_object_or_404(
            Subscription,
            subscriber=self.request.user,
            user=self.get_user()
        )
        instance.delete()


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
    """Теги: только для администратора"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ингридиенты: только для администратора"""
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
