from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/blogs', views.admin_blogs, name='admin_blogs'),
    path('<slug:username>/<slug:blog_slug>', views.blog_home, name='blog_home'),
    path('<slug:username>/<slug:blog_slug>/<slug:category_slug>', views.blog_category, name='blog_category'),
    path('<slug:username>/<slug:blog_slug>/<slug:category_slug>/<slug:post_slug>', views.blog_post, name='blog_post'),
    path("__reload__/", include("django_browser_reload.urls")),
]