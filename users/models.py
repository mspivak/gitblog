from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from github import Github

from .managers import UserManager
from gh.models import GithubToken


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.EmailField(_("email address"), blank=True, unique=True)
    first_name = None
    last_name = None
    name = models.CharField(max_length=255, blank=True)
    manager = UserManager()

    def __str__(self):
        return self.username

    def get_github_user(self):
        token = GithubToken.get_latest_for(self)
        return Github(token.token).get_user()

