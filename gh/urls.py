from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('callback', views.callback, name='callback'),
    path('hook/<slug:username>/<slug:repo_name>', views.hook, name='hook'),
]