from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('users/create', views.create_user),
    path('wall', views.main_page),
    path('users/login', views.login),
    path('logout', views.logout),
    path('wall/post_message', views.post_message),
    path('wall/post_comment/<int:post_id>', views.post_comment),
]