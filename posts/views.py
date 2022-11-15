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
from django.views.generic.edit import UpdateView

class ListCategory(APIView):
    def get(self,request):
        category=Category.objects.all()
        serializer=CategorySerializer(category,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)
    
    #queryset=Category.objects.all()
    #serializer_class=CategorySerializer
    #permission_classes=(permissions.IsAunthenticated)


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class yourImageView(UpdateView):
    model = Post
    def post(self, request, *args, **kwargs):
        img = self.request.FILES["images"]
        Post.imagess = img
        Post.save()

class PostList(APIView):

    def get(self,request):
        posts=Post.objects.all()
        serializer=PostSerializer(posts,many=True)
        filter_backends = (DynamicSearchFilter,)
        filterset_fields = ['category', 'in_stock']
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return Response(serializer.data)

    def post(self,request):
        serializer=PostSerializer(data=request.data)
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors, status=400)

        #def perform_create(self, serializer):
            #serializer.save(author=self.request.user)

    #queryset= Post.objects.all()
    #serializer_class=PostSerializer
    #filter_backends = (DynamicSearchFilter,)
    #filterset_fields = ['category', 'in_stock']
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

    #def perform_create(self, serializer):
       #serializer.save(author=self.request.user)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise 404

    def get(self, request, pk, format=None):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts)
        permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        posts = self.get_object(pk)
        serializer = PostSerializer(posts, data=request.data)
        permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        #def perform_update(self, serializer):
           #serializer.save(updated_by=self.request.user)

    def delete(self, request, pk, format=None):
        posts = self.get_object(pk)
        posts.delete()
        permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
        return Response(status=204)
    #queryset=Post.objects.all()
    #serializer_class=PostSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,]#IsOwnerOrReadOnly#,IsAdminUser]

    #def perform_update(self, serializer):
        #serializer.save(updated_by=self.request.user)
    

class CommentList(APIView):
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    #queryset=Comment.objects.all()
    #serializer_class=CommentSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise 404

    def get(self, request, pk, format=None):
        comments = self.get_object(pk)
        serializer = CommentSerializer(comments)
        permission_classes=[permissions.IsAuthenticatedOrReadOnly]
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comments = self.get_object(pk)
        serializer = CommentSerializer(comments, data=request.data)
        permission_classes=[permissions.IsAuthenticatedOrReadOnly]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        comments = self.get_object(pk)
        comments.delete()
        permission_classes=[permissions.IsAuthenticatedOrReadOnly]
        return Response(status=204)
    #queryset=Comment.objects.all()
    #serializer_class=CommentSerializer
    
    

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
        print(request.GET)
        post=Post.objects.all()
        
        unpublished=post.filter(published=False)
        published = post.filter(published=True)

        if 'is_publish' not in request.GET:
            return Response(status=400,data='error')

        is_publish=int(request.GET['is_publish'])

        if is_publish:
            serializer=PostSerializer(published, many=True)
            return Response(serializer.data)
        else:
            serializer=PostSerializer(unpublished, many=True)
            return Response(serializer.data)








