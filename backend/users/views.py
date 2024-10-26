from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.pagination import PageNumberAndLimit

from .mixins import PartialUpdateUserMixin
from .models import Subscription
from .serializers import (AvatarSerializer, CustomUserCreateSerializer,
                          SubscriptionSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(PartialUpdateUserMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """Пользователи: CRUD."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberAndLimit
    http_method_names = ['put', 'get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'add_avatar' and self.request.method != 'DELETE':
            return AvatarSerializer
        if self.action == 'create':
            return CustomUserCreateSerializer
        return UserSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        """Получения объекта пользователя, сделавшего запрос."""
        serializer = UserSerializer(
            instance=request.user, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put', 'delete', 'get'],
        detail=False,
        permission_classes=[IsAuthenticated],
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
                instance=request.user, data=request.data,
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

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=PageNumberAndLimit,
    )
    def subscriptions(self, request):
        qs = Subscription.objects.all().filter(user=self.request.user)
        page = self.paginate_queryset(qs)
        if page:
            serializer = SubscriptionSerializer(
                page,
                many=True,
                context={'request': request},
            )
            return self.get_paginated_response(serializer.data)

        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return super().get_object()


class SubscriptionViewSet(mixins.DestroyModelMixin,
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """Подписки: POST, DELETE."""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberAndLimit

    def get_following(self):
        return get_object_or_404(
            User, id=self.kwargs.get('user_id')
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'following': self.get_following()
        })
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            following=self.get_following()
        )

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Http404:
            self.get_following()
            return Response(
                {'detail': "Ошибка подписки"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset,
            user=self.request.user,
            following=self.get_following())
        self.check_object_permissions(self.request, obj)

        return obj
