from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response
from utils.constants import RANDOM_STRING_CHARS, TOKEN_LENGTH


def shorten_url() -> str:
    """Возвращает случайную строку для короткой ссылки"""
    return get_random_string(TOKEN_LENGTH, RANDOM_STRING_CHARS)


def create_cart_txt(content: list):
    """
    Создаёт текстовый документ для корзины покупок.
    Возвращает файл в режиме чтения.
    """
    data = []
    for item in content:
        name = item.get('ingredient__name')
        amount = item.get('amount')
        measurement_unit = item.get('ingredient__measurement_unit')
        data.append(f'{name} -> {amount} {measurement_unit}')
    data = '\n'.join(data)

    return HttpResponse(
        data,
        status=status.HTTP_200_OK,
        headers={
            'Content-Type': 'text/plain,charset=utf8',
            'Content-Disposition': 'attachment; filename=shopping.txt'
        }
    )


def post_delete_instance(serializer_cls, model, request, pk):
    """
    Функция для обработки запросов на
    создание/уничтожение объектов корзины и избранного
    """
    recipe = get_object_or_404(
        Recipe,
        pk=pk
    )
    user = request.user
    if request.method == 'POST':
        serializer = serializer_cls(
            data=request.data,
            context={'recipe': recipe, 'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user, recipe=recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if not model.objects.filter(recipe=recipe, user=user).exists():
        return Response(
            {"detail": f"Рецепт не был в {model.__class__.__name__}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    model.objects.filter(recipe=recipe, user=user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
