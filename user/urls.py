from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('login/', views.login, name='user_login'),
    path('register/', views.register, name='user_register'),
    path('forgot-password', views.forgot_password, name='user_forgot_password'),
    path('logout/', views.logout, name='user_logout')
]
