from django.urls import path
from .views import RegistrationView, ActivationView, LoginView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView, PersonView
from django.views.decorators.cache import cache_page
urlpatterns = [

    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()), 
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()), 
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view()),
    path('persons/', cache_page(60)(PersonView.as_view()))
]
