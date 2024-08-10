from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('check_login/', views.check_login, name='check_login'),
    path('logout/', views.user_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_avatar/', views.change_avatar, name='change_avatar'),
    path('change_username/', views.change_username, name='change_username'),
    path('change_email/', views.change_email, name='change_email')
]
