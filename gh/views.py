import json
import hmac, hashlib
from slugify import slugify

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from github import Github

from .forms import NewBlogForm
from blogs.models import Blog


User = get_user_model()


def get_github_login_url():
    github_app = Github().get_oauth_application(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)
    return github_app.get_login_url() + '&scope=repo user:email'


def github_login(request):
    return redirect(get_github_login_url())


@login_required(login_url='home')
def new(request):
    if request.POST:
        form = NewBlogForm(request.POST)
        if form.is_valid():
            blog_name = form.cleaned_data['name']

            try:
                blog = Blog.objects.filter(owner=request.user, name=blog_name).get()
            except Blog.DoesNotExist:
                blog = Blog.objects.create(
                    owner=request.user,
                    name=blog_name,
                    slug=slugify(blog_name)
                )

            if not blog.category_set.count():
                blog.category_set.create(
                    name='Posts', slug='posts'
                )

            blog.create_on_source()
            blog.save()
            return redirect(blog.post_set.first().get_absolute_url())
    else:
        form = NewBlogForm()
        return render(request, 'gh/new.html', context={'form': form})


def callback(request):

    github_app = Github().get_oauth_application(settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET)

    code = request.GET.get('code')

    login_url = get_github_login_url()

    if not code:
        redirect()

    print(f'Got code {code}')

    token = github_app.get_access_token(code)

    if not token.token:
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

    return redirect('admin_blogs')


def ct_compare(a, b):
    """
    ** From Django source **
    Run a constant time comparison against two strings
    Returns true if a and b are equal.
    a and b must both be the same length, or False is
    returned immediately
    """

    if len(a) != len(b):
        return False

    result = 0
    for ch_a, ch_b in zip(a, b):
        result |= ord(ch_a) ^ ord(ch_b)
    return result == 0


@csrf_exempt
def hook(request, username, repo_slug):

    payload = json.loads(request.body)

    user = User.objects.filter(username=username).first()
    blog = Blog.objects.filter(owner=user, slug=repo_slug).first()

    def verify_signature(signed_request, secret):
        if 'X-Hub-Signature-256' not in signed_request.headers:
            return False

        hash_algo, signature = signed_request.headers
        return hmac.compare_digest(
            hmac.new(
                secret.encode('utf-8'),
                msg=signed_request.body,
                digestmod=hashlib.sha256
            ).hexdigest(),
            signature
        )

    if blog.secret and not verify_signature(request, blog.secret):
        print('ERROR: HMAC verification failed')
        return HttpResponse(status=400)

    repo = user.get_github_user().get_repo(blog.slug)

    changes = {file
               for files in [commit['added'] + commit['modified'] for commit in payload['commits']]
               for file in files if file.endswith('.md')}

    for filepath in changes:
        blog.create_or_update_from_file(
            filepath=filepath,
            content=repo.get_contents(filepath).decoded_content.decode('utf-8')
        )

    for commit in payload['commits']:
        for filepath in commit['removed']:
            print(f'Deletting post for {filepath}')
            blog.post_set.filter(filepath=filepath).delete()

    return HttpResponse(status=204)
