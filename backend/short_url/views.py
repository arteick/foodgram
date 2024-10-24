from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import ShortUrl


class RedirectUrl(APIView):
    """Представление для перенаправления пользователя по короткой ссылке"""
    http_method_names = ['get']

    def get(self, request, format=None, slug=None):
        url = get_object_or_404(
            ShortUrl,
            short_url=request.build_absolute_uri()
        ).full_url
        return HttpResponseRedirect(redirect_to=url)
