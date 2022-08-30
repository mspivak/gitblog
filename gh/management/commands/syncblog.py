from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from github import Github

from blogs.models import Blog, Post
from gh.models import GithubToken

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('blog_slug', type=str)

    def handle(self, *args, **options):

        user = User.objects.get(username=options['username'])

        blog = Blog.objects.get(owner=user, slug=options['blog_slug'])

        github = Github(
            GithubToken.get_latest_for(user=user).token
        )

        repo = github.get_user().get_repo(blog.slug)

        for file in repo.get_contents('/'):
            if file.type == 'dir':
                continue

            if file.name.endswith('.md'):

                print(f'Working on {file}')

                slug = file.name.lower()[:-3]
                post = Post.objects.get_or_create(blog=blog, slug=slug)[0]
                post.title = slug.replace('-', ' ').title()
                post.content_md = file.decoded_content.decode('utf-8')
                post.save()


