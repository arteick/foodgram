from django.contrib import admin

from .models import Cart, Favorite, Ingridient, Recipe, Subscription, Tag

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Cart)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(Ingridient)
