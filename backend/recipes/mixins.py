from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


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
