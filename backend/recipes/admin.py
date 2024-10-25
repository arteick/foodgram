from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingCart, Tag)

admin.site.empty_value_display = 'Не задано'


class TagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):

    def _favorite_count(self, obj):
        counter = Favorite.objects.filter(recipe=obj.pk).count()
        return f'{counter} чел.'

    _favorite_count.short_description = 'В избранном у'

    inlines = (
        TagInline,
        IngredientInline
    )

    readonly_fields = ('_favorite_count',)
    list_display = (
        'name',
        'author',
    )
    search_fields = ('author__username', 'name')
    list_filter = ('tags',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
