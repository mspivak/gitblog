from django.conf import settings
from django.db import models
from django.urls import reverse

from github import UnknownObjectException


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    # blog slug is the same as the GitHub repo name
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog_home', kwargs={'username': self.owner.username, 'blog_slug': self.slug})


    @property
    def hook_url(self):
        path = reverse('github_hook', kwargs={'username': self.owner.username, 'repo_slug': self.slug})
        return f'https://{settings.DOMAIN}/{path}'

    def create_on_source(self):

        github_user = self.owner.get_github_user()

        try:
            repo = github_user.get_repo(self.name)
        except UnknownObjectException as e:
            repo = github_user.create_repo(
                self.slug,
                homepage=f'https://{settings.DOMAIN}/{self.get_absolute_url()}',
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

        existing_hook = next((repo for repo in repo.get_hooks() if repo.config['url'] == self.hook_url), None)
        if not existing_hook:
            hook = repo.create_hook(
                name='web',
                config={'url': self.hook_url},
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


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')


class Category(models.Model):
    objects = CategoryManager
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog_category', kwargs={
            'username': self.blog.owner.username,
            'blog_slug': self.blog.slug,
            'category_slug': self.slug,
        })


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

    def previous(self, post: 'Post'):
        return self.get_queryset()\
            .filter(blog__owner=post.blog.owner)\
            .filter(id__lt=post.id)\
            .order_by('-id')\
            .first()

    def next(self, post: 'Post'):
        return self.get_queryset()\
            .filter(blog__owner=post.blog.owner)\
            .filter(id__gt=post.id)\
            .order_by('id')\
            .first()


class Post(models.Model):
    objects = PostManager()
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    content_md = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)
    category = models.ForeignKey('blogs.Category', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('blog_post', kwargs={
            'username': self.blog.owner.username,
            'blog_slug': self.blog.slug,
            'category_slug': self.category.slug,
            'post_slug': self.slug
        })

    def __repr__(self):
        return '<blog>'
