from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect


from .markdown import md_to_html_and_css
from users.models import User
from blogs.models import Blog, Post, Category


def blog_home(request, username, blog_slug):
    blog_owner = User.objects.get(username=username)
    blog = Blog.objects.get(owner=blog_owner, slug=blog_slug)
    categories = blog.category_set.all()

    if request.user.is_authenticated:
        posts = blog.post_set.filter(Q(published_at__isnull=False) | Q(blog__owner=request.user), blog=blog)
    else:
        posts = blog.post_set.filter(published_at__isnull=False, blog=blog)

    return render(request, 'blogs/home.html', context={
        'blog_owner': blog_owner,
        'blog': blog,
        'posts': posts.all(),
        'categories': categories
    })


def blog_category(request, username, blog_slug, category_slug):
    blog_owner = User.objects.get(username=username)
    blog = Blog.objects.get(owner=blog_owner, slug=blog_slug)
    categories = blog.category_set.all()
    category = Category.objects.get(blog=blog, slug=category_slug)
    posts = category.post_set.filter(Q(published_at__not=None) | Q(owner=request.user))

    return render(request, 'blogs/category.html', context={
        'blog_owner': blog_owner,
        'blog': blog,
        'posts': posts,
        'category': category,
        'categories': categories,
    })


def blog_post(request, username, blog_slug, category_slug, post_slug):
    user = User.objects.get(username=username)
    blog = Blog.objects.get(owner=user, slug=blog_slug)
    post = Post.objects.get(blog=blog, slug=post_slug)

    print(post.published_at)
    print(request.user)
    print(user)

    if not post.published_at and request.user != user:
        return HttpResponseNotFound(render(request, 'blogs/notfound.html', context={'blog': blog}))

    categories = blog.category_set.all()

    html, css = md_to_html_and_css(post)

    return render(request, 'blogs/post.html', context={
        'post': post,
        'blog': blog,
        'categories': categories,
        'content': html,
        'content_css': css,
        'next_post': Post.objects.next(post),
        'previous_post': Post.objects.previous(post),
    })


def admin_blogs(request):

    blogs = request.user.blog_set.all()

    if not blogs.count():
        return redirect('github_new')

    return render(request, 'blogs/admin_blogs.html', context={'blogs': blogs})
