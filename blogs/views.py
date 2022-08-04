from django.shortcuts import render

from users.models import User
from blogs.models import Blog, Post


def blog_home(request, username, blog_slug):

    user = User.objects.get(username=username)

    blog = Blog.objects.get(owner=user, slug=blog_slug)

    posts = blog.post_set.all()

    return render(request, 'blogs/blog_home.html', context={'posts': posts, 'user': user})


def blog_post(request, username, blog_slug, post_slug):

    user = User.objects.get(username=username)

    blog = Blog.objects.get(owner=user, slug=blog_slug)

    post = Post.objects.get(blog=blog, slug=post_slug)

    return render(request, 'blogs/blog_post.html', context={'post': post})
