from django.urls import path, include

from . import views

urlpatterns = [
    path('<slug:username>/<slug:blog_slug>', views.blog_home, name='home'),
    path('<slug:username>/<slug:blog_slug>/<slug:category_slug>', views.blog_category, name='category'),
    path('<slug:username>/<slug:blog_slug>/<slug:category_slug>/<slug:post_slug>', views.blog_post, name='post'),
    path("__reload__/", include("django_browser_reload.urls")),
]