from django.urls import path
from . import views

urlpatterns = [
    path('', views.following_timeline, name='home'),
    path('create_post/', views.create_post, name='create_post'),
]