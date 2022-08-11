import os
from slugify import slugify

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from github import Github, UnknownObjectException

from .forms import NewBlogForm
from blogs.models import Blog, Post

github_app = Github().get_oauth_application(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)

User = get_user_model()


def get_github_login_url():
    return github_app.get_login_url() + '&scope=repo user:email'


def github_login(request):
    return redirect(get_github_login_url())


@login_required(login_url='home')
def new(request):

    if request.POST:
        form = NewBlogForm(request.POST)
        if form.is_valid():
            blog = Blog(
                owner=request.user,
                slug=slugify(form.cleaned_data['name']),
                name=form.cleaned_data['name'],
            )
            blog.save()
            return redirect(blog.url)
    else:
        form = NewBlogForm()

    return render(request, 'gh/new.html', context={'form': form})


def callback(request):

    code = request.GET.get('code')

    login_url = get_github_login_url()

    if not code:
        redirect()

    print(f'Got code {code}')

    token = github_app.get_access_token(code)

    if not token.token:
        # raise Exception(f'Code is invalid or expired, please go to {login_url}')
        return HttpResponseRedirect(redirect_to=login_url)

    print(f'Got token {token.token}')

    github = Github(token.token)

    github_user = github.get_user()

    user = User.objects.filter(username=github_user.login).first()

    if not user:
        user = User(
            username=github_user.login,
            email=github_user.email,
            name=github_user.name,
        )
        user.save()

    user.githubtoken_set.create(
        token=token.token
    )

    login(request, user)

    return redirect('new')


def hook(request):
    print('INCOMING REQUEST', request)