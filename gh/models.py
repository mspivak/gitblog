from django.db import models


class GithubToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'<GithubToken {self.token[:6]}>'
