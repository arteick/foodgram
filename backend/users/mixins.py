from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class PartialUpdateUserMixin:
    """
    Миксин обновления объекта модели пользователя.
    Всегда обновляет модель частично.
    """
    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
