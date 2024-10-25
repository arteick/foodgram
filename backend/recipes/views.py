from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from short_url.models import ShortUrl
from short_url.serializers import ShortUrlSerializer
from utils.services import create_cart_txt, shorten_url

from .filters import IngridientFilter, RecipeFilter
from .mixins import CreateDestroyMixin, FullUpdateMixin
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pagination import RecipePageNumberLimit
from .permissions import IsAuthorOrAuthenticatedOrRead
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, OutputRecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги: CRUD только для администратора, GET для всех"""
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Ингридиенты: CRUD только для администратора, GET для всех"""
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngridientFilter


class CartViewSet(CreateDestroyMixin,
                  viewsets.GenericViewSet):
    """Корзина: POST, DELETE"""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)


class FavoriteViewSet(CreateDestroyMixin,
                      viewsets.GenericViewSet):
    """Избранное: POST, DELETE"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)


class RecipeViewSet(FullUpdateMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Рецепты: CRUD"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    queryset = Recipe.objects.all()
    pagination_class = RecipePageNumberLimit
    permission_classes = [IsAuthorOrAuthenticatedOrRead]
    http_method_names = ['patch', 'get', 'post', 'delete']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        data = {'user': self.request.user, 'recipe': serializer.instance}
        Favorite.objects.create(**data)
        ShoppingCart.objects.create(**data)
        serializer.data['is_favorited'] = True
        serializer.data['is_in_shopping_cart'] = True

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return OutputRecipeSerializer
        return CreateRecipeSerializer

    def get_queryset(self):
        recipes = Recipe.objects.all()
        user = self.request.user
        if user.is_anonymous:
            user = -1
        shopping_cart = ShoppingCart.objects.filter(
            recipe_id=OuterRef('pk'),
            user=user
        )
        favorite = Favorite.objects.filter(
            recipe_id=OuterRef('pk'),
            user=user
        )

        return recipes.annotate(
            is_favorited=Exists(favorite),
            is_in_shopping_cart=Exists(shopping_cart),
        )

    @action(
        ['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        recipe_ids = [
            item['recipe_id']
            for item in request.user.shopping_cart.values('recipe_id')
        ]
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=recipe_ids
        ).values('amount', 'ingredient__name', 'ingredient__measurement_unit')
        data = create_cart_txt(ingredients)
        response = HttpResponse(
            data,
            status=status.HTTP_200_OK,
            headers={
                'Content-Type': 'text/plain',
                'Content-Disposition': 'attachment; filename="shopping.txt"'
            }
        )
        return response

    @action(
        ['get'],
        detail=True,
        url_path='get-link'
    )
    def get_link(self, request, pk=None):
        absolute_uri = request.build_absolute_uri()
        domain = absolute_uri.split('api/')[0]
        short_link = domain + 's/' + shorten_url() + '/'
        serializer = ShortUrlSerializer(data={'short_url': short_link})

        if (serializer.is_valid(raise_exception=True)
                and not ShortUrl.objects.filter(full_url=absolute_uri)
                .exists()):

            serializer.save(
                full_url=absolute_uri,
                short_url=short_link
            )

        else:
            short_link = get_object_or_404(
                ShortUrl,
                full_url=absolute_uri
            ).short_url
        return Response({'short-link': short_link}, status=status.HTTP_200_OK)
