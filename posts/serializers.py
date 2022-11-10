from rest_framework import serializers
from .models import Post, Category,Comment
#from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):

  
    class Meta:
        model=Category
        fields=[
            'id',
            'categoryname',
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    #author= serializers.CharField(source='author.username',read_only=True)
    def create(self,validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.body=validated_data.get('body',instance.body)
        instance.author=validated_data.get('author',instance.author)
        instance.post=validated_data.get('post',instance.post)
        

        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ['body', 'author','post']


class PostSerializer(serializers.ModelSerializer):
    #author=serializers.ReadOnlyField(source='author.username')
    images=serializers.ImageField(max_length=None,use_url=True)
    #comments=serializers.PrimaryKeyRelatedField()
    comments=CommentSerializer(many=True,read_only=True)

    
    author = serializers.SlugRelatedField(
       read_only=True,
       slug_field='username',
   )
    updated_by = serializers.SlugRelatedField(
       read_only=True,
       slug_field='username',
   )
  
    category=serializers.CharField(source='category.categoryname',required=False)

    def create(self,validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.content=validated_data.get('content',instance.content)
        instance.images=validated_data.get('images',instance.images)
        instance.category=validated_data.get('category',instance.category)

        instance.save()
        return instance

    class Meta:
        model=Post
        fields=[
            'id','title','content', 'author', 'images','category','comments','updated_by','published',
        ]
    



