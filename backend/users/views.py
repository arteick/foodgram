from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import SetPasswordSerializer
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.pagination import PageNumberAndLimit

from .mixins import UserUpdateModelMixin
from .models import Subscription
from .serializers import (AvatarSerializer, CustomUserCreateSerializer,
                          SubscriptionSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(UserUpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Пользователи: CRUD."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberAndLimit

    def get_request_user(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.request.user.id)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=None,
    )
    def me(self, request):
        """Получения объекта пользователя, сделавшего запрос."""
        serializer = UserSerializer(
            instance=self.get_request_user(), context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put', 'delete', 'get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=None,
        url_path='me/avatar'
    )
    def add_avatar(self, request):
        """Добавить/удалить/посмотреть изображение профиля"""
        if self.request.method == 'PUT':
            return self.partial_update(request)

        if self.request.method == 'DELETE':
            self.request.data['avatar'] = None
            self.partial_update(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if self.request.method == 'GET':
            serializer = self.get_serializer(
                instance=self.get_request_user(), data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 

    @action(
        ['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def set_password(self, request):
        """Изменение пароля"""
        serializer = SetPasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if (self.action == 'add_avatar' and self.request.method == 'PUT' or
           self.action == 'add_avatar' and self.request.method == 'GET'):
            return AvatarSerializer
        if self.action == 'create':
            return CustomUserCreateSerializer
        return UserSerializer


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

    def create(self, request, *args, **kwargs): # Можно это убрать и переписать методы сериализатора
        user = self.get_user()
        serializer = self.get_serializer(
            data=request.data, context={'request': request, 'user': user}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = UserSerializer(
            instance=user, context={'request': request}
        )
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