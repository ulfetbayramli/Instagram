from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from . import views
from .views import HomePage, Register, ProfilePage

# app_name = 'users'


urlpatterns = [ 
    path('account_list', views.account_list, name='home_page'),

    # path('account', views.HomePage, name='home_page'),
    path('profile', views.ProfilePage, name='profile_page'),

    path('register/', views.Register.as_view(), name='register'),
    path('confirmation/<str:uuidb64>/<str:token>/', views.confirmation, name='confirmation'),

    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]