from django.db import models
from django.conf import settings
from django.urls import reverse

from github import UnknownObjectException

from blogs.models import Blog


class GithubToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'<GithubToken {self.token[:6]}>'

    @classmethod
    def get_latest_for(cls, user):
        return cls.objects.filter(user=user).order_by('-created_at').first()


class GithubBlog(Blog):

    @property
    def hook_url(self):
        path = reverse('hook', kwargs={'username': self.owner.username, 'repo_slug': self.slug})
        return f'https://{settings.DOMAIN}/{path}'

    def create_on_source(self):

        github_user = self.owner.get_github_user()

        try:
            repo = github_user.get_repo(self.name)
        except UnknownObjectException as e:
            repo = github_user.create_repo(
                self.slug,
                homepage=f'https://{settings.DOMAIN}/{self.url}',
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

        existing_hook = next((repo for repo in repo.get_hooks() if repo.config['url'] == repo.hook_url), None)
        if not existing_hook:
            hook = repo.create_hook(
                name='web',
                config={'url': repo.hook_url},
                active=True,
                events=['push']
            )
            print('Created hook', hook)

    def update_from_source(self):
        pass
    # s3 = boto3.client('s3')
    #
    # files = github.get_repo(self.name).get_contents('/')
    #
    # for file in files:
    #     if file.name.endswith('.md'):
    #
    #     md = base64.b64decode(file.content).decode('utf-8')
    #
    #     filename = file.name.removesuffix('.md')
    #
    #     s3.put_object(Body=rendered_html,
    #                   Bucket='gitblog-html',
    #                   Key= f'{repo_name}/{filename}.html')
