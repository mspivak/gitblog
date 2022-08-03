import os

from django.conf import settings
from django.shortcuts import render

from github import Github

github_app = Github().get_oauth_application(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)


def get_github_login_url():
    return github_app.get_login_url() + '&scope=repo'


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
        raise Exception(f'Code is invalid or expired, please go to {login_url}')

    print(f'Got token {token.token}')

    github = Github(token.token)

    user = github.get_user()

    print(user, user.name)

    print([repo for repo in user.get_repos()])

    repo_name = 'my-gitblog'

    print(f'https://{request.get_host}/gh/{user.name}/{repo_name}/hook')

    repo = user.create_repo(
        repo_name,
        # homepage=f'https://{request.get_host}/{user.login}/{repo_name}',
        # private=True,
        # auto_init=False,
        # has_issues=False,
        # has_projects=False,
        # has_wiki=False,
        # has_downloads=False,
    )

    repo.create_file(
        path='README.md',
        message='Initial commit',
        content=f'# Welcome to Gitblog. Gitblog publishes your markdown files as blog posts nice and easy.'
    )

    repo.create_hook(
        name='web',
        config={'url': f'https://{request.get_host}/gh/{user.name}/{repo_name}/hook'},
        active=True,
        events=['push'],
    )



    return {
        'repos': [repo for repo in github.get_repos()]
    }

