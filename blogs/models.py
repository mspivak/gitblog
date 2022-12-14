import boto3
import misaka
import secrets
import uuid
import urllib.request, urllib.parse
from github.GithubException import UnknownObjectException
from slugify import slugify
from bs4 import BeautifulSoup

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .markdown import SyncRenderer


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    # blog slug is the same as the GitHub repo name
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # Github webhook secret
    secret = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'slug'], name='unique_owner_slug'),
        ]

    def __str__(self):
        return f'Blog #{self.id} - {self.owner.username}/{self.slug}'

    def save(self, **kwargs):
        # Updates old posts.
        if not self.secret:
            self.secret = secrets.token_urlsafe(32)
        super(Blog, self).save()

    def get_absolute_url(self):
        return reverse('blog_home', kwargs={'username': self.owner.username, 'blog_slug': self.slug})

    @property
    def hook_url(self):
        path = reverse('github_hook', kwargs={'username': self.owner.username, 'repo_slug': self.slug})
        return f'https://{settings.DOMAIN}{path}'

    def create_on_source(self):

        github_user = self.owner.get_github_user()

        try:
            repo = github_user.get_repo(self.slug)
        except UnknownObjectException:

            blog_url = f'https://{settings.DOMAIN}{self.get_absolute_url()}'

            repo = github_user.create_repo(
                self.slug,
                homepage=blog_url,
                private=True,
                auto_init=False,
                has_issues=False,
                has_projects=False,
                has_wiki=False,
                has_downloads=False,
            )

            with open('blogs/default_post.md', 'r') as file:
                first_post_md = file.read()

            repo.create_file(
                path='README.md',
                message='Initial commit',
                content=first_post_md.format_map({
                    'owner': self.owner.username,
                    'repo_slug': self.slug,
                    'blog_name': self.name,
                    'blog_url': blog_url
                })
            )

        existing_hook = next((repo for repo in repo.get_hooks() if repo.config['url'] == self.hook_url), None)
        if not existing_hook:
            self.secret = secrets.token_urlsafe(32)
            self.save()
            hook = repo.create_hook(
                name='web',
                config={
                    'url': self.hook_url,
                    'content_type': 'json',
                    'secret': self.secret,
                },
                active=True,
                events=['push']
            )
            print('Created hook', hook)

        self.sync()

    def sync(self):
        repo = self.get_github_repo()

        repo_tree = repo.get_git_tree(
            sha=repo.get_branch(repo.default_branch).commit.sha,
            recursive=True
        ).tree

        for element in repo_tree:
            if element.type != 'blob':
                continue
            filepath = element.path
            if filepath.endswith('.md'):
                self.create_or_update_from_file(
                    filepath=filepath,
                    content=repo.get_contents(filepath).decoded_content.decode('utf-8')
                )

        print('Looking for deleted posts')
        for post in self.post_set.all():
            print(post.filepath)
            if post.filepath not in [element.path for element in repo_tree]:
                print(f'- Deletting {post}')
                post.delete()

    def create_or_update_from_file(self, filepath, content):
        print(f'Working on {filepath}')
        slug = slugify(filepath.split('/')[-1].lower()[:-3])
        post = Post.objects.get_or_create(blog=self, slug=slug)[0]
        post.category = self.get_or_create_category_from_filepath(filepath)
        post.published_at = timezone.now() if filepath.startswith('public/') else None
        post.filepath = filepath
        post.title = post.slug.replace('-', ' ').title()
        post.content_md = content
        post.save()

        print('Parsing and uploading related files')
        renderer = SyncRenderer(blog=self)
        to_html = misaka.Markdown(renderer)
        content_html = to_html(post.content_md)
        print(f'- Extracted files: {renderer.extracted_files}')

        for file in renderer.extracted_files:
            file.upload()

        post.summary = self.extract_summary_from_html(content_html)
        post.save()

        return post

    def extract_summary_from_html(self, html):

        paragraphs = BeautifulSoup(html, features="html.parser")('p')

        if len(paragraphs):
            return paragraphs[0].get_text()

        return ''

    def get_or_create_category_from_filepath(self, filepath):
        parts = filepath.split('/')

        if len(parts) == 3 and parts[0] == 'public':
            category_slug = parts[1]
            category = self.category_set.get_or_create(
                slug=category_slug,
                defaults={'name': category_slug.title()}
            )
        else:
            category = self.category_set.first()

        return category

    def get_github_repo(self):
        return self.owner.get_github_user().get_repo(self.slug)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('name')


class Category(models.Model):

    objects = CategoryManager
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['blog', 'slug'], name='unique_blog_category_slug'),
        ]

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
            .filter(blog=post.blog)\
            .filter(id__lt=post.id)\
            .order_by('-id')\
            .first()

    def next(self, post: 'Post'):
        return self.get_queryset()\
            .filter(blog=post.blog)\
            .filter(id__gt=post.id)\
            .order_by('id')\
            .first()


class Post(models.Model):
    objects = PostManager()
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=255)
    summary = models.TextField(default='')
    filepath = models.CharField(max_length=255)
    content_md = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Public URL access token
    access_token = models.CharField(max_length=255)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)
    category = models.ForeignKey('blogs.Category', on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog', 'slug'], name='unique_blog_post_slug'),
        ]

    def save(self, **kwargs):
        # Updates old posts.
        if not self.access_token:
            self.access_token = secrets.token_urlsafe(32)
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse('blog_post', kwargs={
            'username': self.blog.owner.username,
            'blog_slug': self.blog.slug,
            'category_slug': self.category.slug,
            'post_slug': self.slug
        })

    def get_shareable_url(self):
        url =  self.get_absolute_url()
        params = urllib.parse.urlencode({'token': self.access_token})
        return f'https://{settings.DOMAIN}{url}?{params}'


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    repo_path = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    alt = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey('blogs.Blog', on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url =  f'https://{settings.AWS_USER_FILES_BUCKET_NAME}.s3.amazonaws.com/{self.object_key}'

    @property
    def object_key(self):
        return f'{self.blog.owner.username}/{self.blog.slug}/{self.repo_path}'

    def upload(self):

        print(f'Downloading {self} from Github: {self.blog} {self.repo_path}')
        github_file = self.blog.get_github_repo().get_contents(f'/{self.repo_path}')
        if github_file.content:
            content = github_file.decoded_content
        else:
            # File size is over 1MB, do a second request to get it
            with urllib.request.urlopen(github_file.download_url) as raw_file:
                content = raw_file.read()

        print(f'Uploading {self} from to s3://{settings.AWS_USER_FILES_BUCKET_NAME}/{self.object_key}')
        boto3.client('s3').put_object(
            Body=content,
            Bucket=settings.AWS_USER_FILES_BUCKET_NAME,
            Key=self.object_key
        )
