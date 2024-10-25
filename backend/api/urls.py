from django.urls import include, path, re_path
from recipes.views import (CartViewSet, FavoriteViewSet, IngredientViewSet,
                           RecipeViewSet, TagViewSet)
from rest_framework.routers import DefaultRouter
from users.views import SubscriptionViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'ingredients', IngredientViewSet),

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'recipes/(?P<recipe_id>\d+)/shopping_cart/', CartViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    re_path(r'users/(?P<user_id>\d+)/subscribe', SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    re_path(r'recipes/(?P<recipe_id>\d+)/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('auth/', include('djoser.urls.authtoken')),
]
