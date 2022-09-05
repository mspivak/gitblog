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

        blog.sync()


