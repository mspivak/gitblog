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

    def create_or_update_from_file(self, filepath, content):
        print(f'Working on {filepath}')
        slug = filepath.split('/')[-1].lower()[:-3]
        post = Post.objects.get_or_create(blog=self, slug=slug)[0]
        post.category = self.get_or_create_category_from_filepath(filepath)

        # post.published = filepath.startswith('public/')

        post.filepath = filepath
        post.title = post.slug.replace('-', ' ').title()
        post.content_md = content
        post.save()
        return post

    def get_or_create_category_from_filepath(self, filepath):
        parts = filepath.split('/')

        if len(parts) == 3 and parts[0] == 'public':
            category_slug = parts[1]
            category = self.category_set.get_or_create(slug=category_slug)
        else:
            category = self.category_set.order_by('created_at').first

        return category


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
    filepath = models.CharField(max_length=255)
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
