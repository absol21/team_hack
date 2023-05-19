from django.urls import path, include
from .views import CategoryListView, PostViewSet, CommentView
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentView)
router.register('categories', CategoryListView)
# router.register('favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]