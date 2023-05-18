from django.urls import path, include
from .views import CategoryListView, PostViewSet, CommentView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentView)
# router.register('favorites', FavoriteViewSet)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('', include(router.urls)),
]