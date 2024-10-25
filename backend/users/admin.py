from django.contrib import admin

from .models import CustomUser, Subscription


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('email', 'username')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Subscription)
