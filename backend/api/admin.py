from django.contrib import admin

from .models import (Favorite, Ingridient, Recipe, RecipeIngridient,
                     ShoppingCart, Subscription, Tag, CustomUser)

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(Ingridient)
admin.site.register(RecipeIngridient)
admin.site.register(CustomUser)
