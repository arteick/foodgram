from django.contrib import admin

from .models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    """Настройки админки для модели коротких ссылок"""
    list_display = (
        'full_url',
        'short_url',
        'created_at',
        'is_active'
    )
    search_fields = ('full_url', 'short_url')
    ordering = ('-created_at',)
    empty_value_display = 'Не задано'
