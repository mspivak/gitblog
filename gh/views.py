import json
from slugify import slugify

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from github import Github

from .forms import NewBlogForm
from blogs.models import Blog, Post
from gh.models import GithubToken

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
            blog.create_on_source()
            blog.save()
            return redirect(blog.get_absolute_url())
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

    return redirect('github_new')


@csrf_exempt
def hook(request, username, repo_slug):
    payload = json.loads(request.POST['payload'])

    user = User.objects.filter(username=username).first()
    blog = Blog.objects.filter(owner=user, slug=repo_slug).first()

    github = Github(
        GithubToken.get_latest_for(user=user).token
    )

    repo = github.get_user().get_repo(blog.slug)

    changes = {file
               for files in [commit['added'] + commit['modified'] for commit in payload['commits']]
               for file in files if file.endswith('.md')}

    for file in changes:
        print(f'Working on {file}')
        slug = file.split('/')[-1].lower()[:-3]
        post = Post.objects.get_or_create(blog=blog, slug=slug)[0]
        post.filepath = file
        post.title = post.slug.replace('-', ' ').title()

        content = repo.get_contents(file)

        print(content)


        post.content_md = content.decoded_content.decode('utf-8')
        post.save()

    return HttpResponse(status=204)