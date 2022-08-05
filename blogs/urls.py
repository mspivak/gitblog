from django.urls import path

from . import views

urlpatterns = [
    path('<slug:username>/<slug:blog_slug>', views.blog_home, name='blog_home'),
    path('<slug:username>/<slug:blog_slug>/<slug:post_slug>', views.blog_post, name='blog_post'),
]