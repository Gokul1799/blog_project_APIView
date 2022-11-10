from django.shortcuts import render
from rest_framework import serializers
from .models import Post, Category,Comment

from rest_framework import generics, permissions,filters
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import PostSerializer,CategorySerializer,CommentSerializer
from django.contrib.auth.models import User
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

class ListCategory(generics.ListCreateAPIView):
    
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    #permission_classes=(permissions.IsAunthenticated)


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class PostList(generics.ListCreateAPIView):

    queryset= Post.objects.all()
    serializer_class=PostSerializer
    filter_backends = (DynamicSearchFilter,)
    filterset_fields = ['category', 'in_stock']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]#IsOwnerOrReadOnly#,IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    

class CommentList(generics.ListCreateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class PublishPost(APIView):
    def patch(self,request):
        post_id=request.data['id']
        post=Post.objects.get(id=post_id)
        post.published=True
        post.save()
        blog=PostSerializer(post)
        return Response(data=blog.data,status=200)

class ListPublish(APIView):
    def get(self,request):
        #post=Post.objects.all()
        a=[]
        unpublished=[]
        for post in Post.objects.all():
            if post.published==True:
                
                blog=PostSerializer(post)
                a.append(blog.data)
            else:
                blog=PostSerializer(post)
                unpublished.append(blog.data)

        return Response(a)


class ListUnpublished(APIView):
    def get(self,request):
        unpublished=[]
        for post in Post.objects.all():
            if post.published==False:
                blog=PostSerializer(post)
                unpublished.append(blog.data)
        return Response(unpublished)




