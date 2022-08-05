from typing import Union

from django.db import models
from django.urls import reverse


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    # blog slug is the same as the GitHub repo name
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    @property
    def url(self):
        return f'/{self.owner.username}/{self.slug}'


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')


class Category(models.Model):
    objects = CategoryManager
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)

    @property
    def url(self):
        return f'{self.blog.url}/{self.slug}'

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def previous(self, post: 'Post'):
        return self.get_queryset()\
            .filter(blog__owner=post.blog.owner)\
            .filter(id__lt=post.id)\
            .order_by('-id')\
            .first()

    def next(self, post: 'Post'):
        return self.get_queryset()\
            .filter(blog__owner=post.blog.owner)\
            .filter(id__gt=post.id)\
            .order_by('id')\
            .first()


class Post(models.Model):
    objects = PostManager()
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    content_md = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)
    category = models.ForeignKey('blogs.Category', on_delete=models.SET_NULL, null=True)

    @property
    def url(self):
        return reverse('post', kwargs={
            'username': self.blog.owner.username,
            'blog_slug': self.blog.slug,
            'category_slug': self.category.slug,
            'post_slug': self.slug
        })
