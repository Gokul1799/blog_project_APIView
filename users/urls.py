from .views import RegisterAPI
from django.urls import path
from . import views
from .views import UserList,UserDetail

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]