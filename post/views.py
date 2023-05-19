from rest_framework import generics, filters
from .models import Category, Post, Rating, Like, Favorite, Comment
from rest_framework import viewsets
from .serializers import CategorySerializer, PostSerializer, RatingSerializer, CommentCreateSerializer#, FavoriteSerializer
from .permissions import IsOwnerPermission, IsAdminOrActivePermission
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from PIL import Image
from io import BytesIO

from .tasks import some_func



class CategoryListView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    @action(methods =['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['posts'] = pk
        rating = Rating.objects.filter(author=request.user, post=pk).first()
        # print(data['post'])
        serializer = RatingSerializer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response('вы уже оставили рейтинг используйте PATCH запрос')
            elif rating and request.method == 'PATCH':
                rating = Rating.objects.filter(pk=pk, author=request.user)
                serializer.update(rating, serializer.validated_data)
                return Response('updated', status=204)
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data, status=201)
            
    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.delete()
            message = 'disliked'
        except Like.DoesNotExist:
            like = Like.objects.create(post=post, author=user, is_liked=True)
            like.save()
            message = 'liked'
        return Response(message, status=201)

    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            favorite = Favorite.objects.get(post=post, author=user)
            favorite.delete()
            message = 'unfavorited'
        except Favorite.DoesNotExist:
            favorite = Favorite.objects.create(post=post, author=user, is_favorite=True)
            favorite.save()
            message = 'favorited'
        return Response(message, status=201)

    @action(['POST'], detail=True)
    def process_image(self, request, pk=None):
        post = self.get_object()

        # Получить изображение из запроса
        image_file = request.FILES.get('image')
        if not image_file:
            return Response('No image provided. Image processing skipped.', status=200)

        # Открыть изображение с помощью Pillow
        try:
            image = Image.open(image_file)
        except Exception as e:
            return Response(str(e), status=400)

        # Произвести необходимую обработку изображения
        # Например, изменить размер изображения
        image.thumbnail((1600, 1900))

        # Сохранить обработанное изображение в памяти
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        # Сохранить изображение в поле ImageField модели Post
        post.image.save(image_file.name, output)

        return Response('Image processed and saved', status=200)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrActivePermission]
        elif self.action in ['list', 'retrive']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

# class FavoriteViewSet(viewsets.ModelViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = request.user
    #     post = serializer.validated_data.get('post')
    #     if Favorite.objects.filter(user=user, post=post).exists():
    #         return Response({"message": "Post is already in favorites"}, status=201)
    #
    #     favorite = serializer.save(user=user, is_favorite=True)
    #     return Response(serializer.data, status=201)

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer


@api_view(['GET'])
def some_view(request):
    some_func.delay()
    return Response("celery запустил эту функцию", 200)

