from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (CartViewSet, FavoriteViewSet, IngridientViewSet,
                    RecipeViewSet, SubscriptionViewSet, TagViewSet,
                    UserViewSet
)

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart', CartViewSet)
router.register(r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet)
router.register(r'ingridients', IngridientViewSet),

urlpatterns = [
    re_path(r'users/(?P<user_id>\d+)/subscribe', SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
