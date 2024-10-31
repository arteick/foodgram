from rest_framework import serializers
from short_url.models import ShortUrl


class ShortUrlSerializer(serializers.ModelSerializer):
    """Сериализатор для коротких ссылок"""

    class Meta:
        model = ShortUrl
        fields = ('short_url',)
        read_only_fields = ('short_url',)
