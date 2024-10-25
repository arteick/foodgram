from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import Recipe


class CreateDestroyMixin(CreateModelMixin, DestroyModelMixin):
    """
    Миксин для вьюсетов корзины покупок и избранного.
    Добавляет в контекст объекты request и recipe.
    Изменяет метод perform_create
    """

    def get_recipe(self):
        return get_object_or_404(
            Recipe, id=self.kwargs.get('recipe_id')
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request, 'recipe': self.get_recipe()})
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            recipe=self.get_recipe()
        )

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        recipe = self.get_recipe()
        try:
            obj = get_object_or_404(
                queryset,
                user=self.request.user,
                recipe=recipe)
        except Http404:
            message = 'Ошибка, рецепт не был в корзине покупок'
            if 'Favorite' in self.__class__.__name__:
                message = 'Ошибка, рецепт не был добавлен в избранное'
            return Response(
                {'detail': message},
                status=HTTP_400_BAD_REQUEST
            )
        self.check_object_permissions(self.request, obj)
        return obj


class FullUpdateMixin(UpdateModelMixin):
    """
    Миксин обновления объекта модели.
    Всегда обновляет модель только целиком.
    """
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=False
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=HTTP_200_OK)
