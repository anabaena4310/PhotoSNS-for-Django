from django.urls import path
from . import views

urlpatterns = [
    path('', views.following_timeline, name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('follow_unfollow_user/<int:id>/', views.follow_unfollow_user, name='follow_unfollow_user'),
]