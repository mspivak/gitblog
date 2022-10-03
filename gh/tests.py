from unittest.mock import patch

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from users.models import User
from gh.models import GithubToken

from github.Requester import Requester
from github.AuthenticatedUser import AuthenticatedUser

MOCK_GITHUB_CALLBACK_CODE = '123123123'
MOCK_GITHUB_CALLBACK_TOKEN = 'TOKEN_ABCABCABC123123123'


class MockGithubAccessToken:
    token = MOCK_GITHUB_CALLBACK_TOKEN


mock_github_requester = Requester(
    login_or_token='someusername',
    password='password',
    jwt='bla',
    pool_size=10,
    base_url='http://githubbloggingurl.com',
    timeout=120,
    user_agent='Mock',
    per_page=100,
    verify=False,
    retry='bla',
)


class MockGithubApp:

    def get_login_url(self):
        return 'http://githubloginurl.com'

    def get_access_token(self, code):
        if code == MOCK_GITHUB_CALLBACK_CODE:
            return MockGithubAccessToken()
        raise Exception('Incorrect mocking Github code')

    def get_repo(self):
        return


class MockGithub():

    def __init__(self, token=None):
        self.token = token

    def get_oauth_application(self, client_id, client_secret):
        return MockGithubApp()

    def get_user(self):
        return AuthenticatedUser(
            requester=mock_github_requester, headers={}, completed=True,
            attributes={
                'login': 'someusername',
                'name': 'somename',
                'email': 'someuser@someserver.com',
            }
        )

class GithubTestCase(TestCase):

    def test_github_redirect_url(self):
        response = self.client.get('/github/')
        self.assertEqual(response.status_code, 302)
        try:
            URLValidator()(response.url)
        except ValidationError:
            self.fail('Invalid Github login URL')

    def test_github_callback(self):

        with patch('gh.views.Github', MockGithub):
            response = self.client.get('/github/callback/', {'code': MOCK_GITHUB_CALLBACK_CODE})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('admin_blogs'))

        github_user = MockGithub().get_user()

        user = User.objects.get(username=github_user.login, email=github_user.email)

        self.assertEqual(GithubToken.get_latest_for(user).token, MOCK_GITHUB_CALLBACK_TOKEN)
        self.assertEqual(user.name, github_user.name)

    # def test_github_hook(self):
    #
    #     with patch()

