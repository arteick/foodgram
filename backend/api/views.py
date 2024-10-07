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
from .models import Cart, Favorite, Ingridient, Recipe, Subscription, Tag
from .pagination import PageNumberAndLimit
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngridientSerializer, RecipeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Пользователи: CRUD."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberAndLimit

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        url_name='me'
    )
    def me(self, request):
        """Получение своей учетной записи."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put', 'delete'],
        detail=False,
        permissions_classes=[IsAuthenticated],
        url_path='me/avatar/',
        url_name='set_avatar'
    )
    def add_avatar(self, request):
        """Добавление изображения профиля."""
        serializer = UserSerializer(
            request.user, data=request.data,
            partial=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """Подписки: получение, добавление, удаление."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberAndLimit  # Мб придётся переписать
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
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class RecipeViewSet(CustomUpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
