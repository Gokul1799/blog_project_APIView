from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # code omitted for brevity
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('category-list',ListCategory.as_view(), name='category-list'),
    #path('category-detail/<int:pk>', DetailCategory.as_view(), name='category-detail'),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('post_publish',views.PublishPost.as_view()),
    path('list_publish',views.ListPublish.as_view()),
    #path('list_unpublish',views.ListUnpublished.as_view()),
]