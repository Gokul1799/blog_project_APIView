from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    categoryname=models.CharField(max_length=200)

    def __str__(self):
        return self.categoryname

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    images=models.ImageField(null=True, blank=True, upload_to="images/")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE,blank=True,null=True)
    updated_by=models.ForeignKey('auth.User', related_name='post', on_delete=models.CASCADE,blank=True,null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)
    published=models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.title

    #def get_absolute_url(self):
        #return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    body=models.TextField(blank=False)
    author=models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post=models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)

    class Meta:
        ordering=['created']



