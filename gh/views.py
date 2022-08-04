import os

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect
from django.shortcuts import render

from github import Github, UnknownObjectException

from blogs.models import Blog, Post

github_app = Github().get_oauth_application(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)

User = get_user_model()


def get_github_login_url():
    return github_app.get_login_url() + '&scope=repo user:email'


def home(request):

    print(os.getenv('GITHUB_CLIENT_ID'))

    return render(request, 'gh/home.html', context={'login_url': get_github_login_url()})


def callback(request):

    code = request.GET.get('code')

    login_url = get_github_login_url()

    if not code:
        return {
            'login_url': login_url
        }

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

    token = user.githubtoken_set.create(
        token=token.token
    )

    repo_name = 'my-gitblog'

    try:
        repo = github_user.get_repo(repo_name)
    except UnknownObjectException as e:
        repo = github_user.create_repo(
            repo_name,
            homepage=f'https://{request.get_host}/{user.username}/{repo_name}',
            private=True,
            auto_init=False,
            has_issues=False,
            has_projects=False,
            has_wiki=False,
            has_downloads=False,
        )
        print('Created repo', repo)
        repo.create_file(
            path='README.md',
            message='Initial commit',
            content=f'# Welcome to Gitblog. Gitblog publishes your markdown files as blog posts nice and easy.'
        )

        blog = Blog(
            owner=user,
            slug=repo_name,
            name=' '.join(repo_name.split('-')).title(),
        )
        blog.save()

    hook_url = f'https://{request.get_host()}/github/hook/{user.username}/{repo_name}'

    existing_hook = next((repo for repo in repo.get_hooks() if repo.config['url'] == hook_url), None)

    if not existing_hook:
        hook = repo.create_hook(
            name='web',
            config={'url': hook_url},
            active=True,
            events=['push']
        )
        print('Created hook', hook)

    login(request, user)

    return HttpResponseRedirect(redirect_to=f'/{user.username}/{repo_name}')


def hook(request):
    print('INCOMING REQUEST', request)