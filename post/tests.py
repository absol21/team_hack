from django.test import TestCase
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category, Like
from .views import PostViewSet
from rest_framework.authtoken.models import Token

User = get_user_model()


class PostTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat1')
        # self.tags = (tag, )
        user = User.objects.create_user(email='user@gmail.com', password='12345', is_active=True, name='test')
        self.token = '12345'
        posts = [
            Post(author=user, title='post', category=self.category, song='song1'),
            Post(author=user, title='post2', category=self.category, song='song2')
        ]
        Post.objects.bulk_create(posts)


    def test_list(self):
        request = self.factory.get('api/v1/posts/')
        view = PostViewSet.as_view({'get': 'list'})
        response = view(request)
        #  print(response)

        assert response.status_code == 200

    def test_retrive(self):
        id = Post.objects.all()[0].id
        request = self.factory.get(f'/posts/{id}/')
        view = PostViewSet.as_view({'get': 'list'})
        response = view(request, pk=id)
        # print(response.data)
        assert response.status_code == 200

    def test_create(self):
        user = User.objects.all()[0]
        data = {
            'title': 'post1',
            'category': 'cat1',
            'song': 'song',
        }
        request = self.factory.post('/posts/', data, format='json')
        force_authenticate(request, user=user, token=self.token)
        view = PostViewSet.as_view({'post': 'create'})
        response = view(request)
        print(response)

        # assert response.status_code==200

    def test_update(self):
        user = User.objects.all()[0]
        data = {
            'title': 'updated title'
        }
        post = Post.objects.all()[1]
        request = self.factory.patch(f'/posts/{post.id}/', data, format='json')
        force_authenticate(request, user=user)
        view = PostViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=post.id)
        # print(response.status_code)
        assert response.status_code == 200
        assert Post.objects.get(id=post.id).title == data['title']

    def test_delete(self):
        user = User.objects.all()[0]
        post = Post.objects.all()[0]
        request = self.factory.delete(f'/posts/{post.id}/')
        force_authenticate(request, user=user)
        view = PostViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=post.id)
        # print(response.status_code)
        assert response.status_code == 204
        assert not Post.objects.filter(id=post.id).exists()
