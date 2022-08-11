from django.urls import path

from . import views

urlpatterns = [
    path('', views.github_login, name='github_login'),
    path('new', views.new, name='github_new'),
    path('callback', views.callback, name='github_callback'),
    path('hook/<slug:username>/<slug:repo_name>', views.hook, name='github_hook'),
]