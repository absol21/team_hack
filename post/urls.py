from django.urls import path, include
from .views import CategoryListView, PostViewSet, CommentView
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

class CachingRouter(DefaultRouter):
    def register(self, prefix, viewset, basename=None):
        super().register(prefix, viewset, basename)

        url = prefix if isinstance(prefix, str) else prefix[0]

        self.urls.append(path(url, cache_page(60 * 15)(viewset.as_view({'get': 'list'})), name=f'{basename}-list'))
        self.urls.append(path(f'{url}/<pk>/', cache_page(60 * 15)(viewset.as_view({'get': 'retrieve'})), name=f'{basename}-detail'))

router = CachingRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentView)
router.register('categories', CategoryListView)
# router.register('favorites', FavoriteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]