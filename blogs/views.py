import markdown
from django.shortcuts import render

from users.models import User
from blogs.models import Blog, Post, Category


def blog_home(request, username, blog_slug):
    user = User.objects.get(username=username)
    blog = Blog.objects.get(owner=user, slug=blog_slug)
    categories = blog.category_set.all()
    posts = blog.post_set.all()

    return render(request, 'blogs/home.html', context={
        'user': user,
        'blog': blog,
        'posts': posts,
        'categories': categories
    })


def blog_category(request, username, blog_slug, category_slug):
    user = User.objects.get(username=username)
    blog = Blog.objects.get(owner=user, slug=blog_slug)
    categories = blog.category_set.all()
    category = Category.objects.get(blog=blog, slug=category_slug)
    posts = category.post_set.all()

    return render(request, 'blogs/category.html', context={
        'user': user,
        'blog': blog,
        'posts': posts,
        'category': category,
        'categories': categories,
    })


def blog_post(request, username, blog_slug, category_slug, post_slug):
    user = User.objects.get(username=username)
    blog = Blog.objects.get(owner=user, slug=blog_slug)
    post = Post.objects.get(blog=blog, slug=post_slug)
    categories = blog.category_set.all()

    content = markdown.markdown(str(post.content_md))

    return render(request, 'blogs/post.html', context={
        'post': post,
        'blog': blog,
        'categories': categories,
        'content': content,
        'next_post': Post.objects.next(post),
        'previous_post': Post.objects.previous(post),
    })
