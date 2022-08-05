from django.urls import path

from . import views

urlpatterns = [
    path('<slug:username>/<slug:blog_slug>', views.blog_home, name='home'),
    path('<slug:username>/<slug:blog_slug>/<slug:category_slug>', views.blog_category, name='category'),
    path('<slug:username>/<slug:blog_slug>/<slug:category_slug>/<slug:post_slug>', views.blog_post, name='post'),
]