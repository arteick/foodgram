from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import SubscriptionViewSet, CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet)
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'ingredients', IngredientViewSet),

urlpatterns = [
    path('', include(router_v1.urls)),
    re_path(r'users/(?P<user_id>\d+)/subscribe', SubscriptionViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'}
    )),
    path('auth/', include('djoser.urls.authtoken')),
]
