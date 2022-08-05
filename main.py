import base64
import boto3
import markdown
from dotenv import load_dotenv
import os

from github import Github

load_dotenv()

repo_name = 'mspivak/my-gitblog'

github = Github('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')

for repo in github.get_user().get_repos():
    print(repo.name)


#
#
# def github_callback(event, context):
#
#     github = Github()
#
#     app = github.get_oauth_application(os.environ['GITHUB_CLIENT_ID'], os.environ['GITHUB_CLIENT_SECRET'])
#
#     # code = event['queryStringParameters'].get('code')
#
#     code =
#
#
#     login_url = app.get_login_url()
#
#     if not code:
#         return {
#             'login_url': login_url
#         }
#
#     print(f'Got code {code}')
#
#     token = app.get_access_token(code)
#
#     if not token.token:
#         raise Exception(f'Code is invalid or expired, please go to {login_url}')
#
#     print(f'Got token {token.token}')
#
#     github = Github('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')
#
#     return {
#         'repos': [repo for repo in github.get_repos()]
#     }


#
#
#
# login_url = app.get_login_url()
#
#
# print(login_url)



s3 = boto3.client('s3')

files = github.get_repo(repo_name).get_contents('/')
#
# with open('template.html', mode='r') as template_file:
#     template = template_file.read()
#
for file in files:

    print(file)
#
#     if file.name.endswith('.md'):
#
        md = base64.b64decode(file.content).decode('utf-8')
#
#         filename = file.name.removesuffix('.md')
#
#         navbar = f'''
#             <nav>
#                 <span>{repo_name}</span>
#                 <ul>
#                     <li><a href="/">Home</a></li>
#                     <li><a href="/posts">Posts</a></li>
#                     <li><a href="/about">About</a></li>
#                 </ul>
#             </nav>
#         '''
#
#         rendered_html = template.format(
#             title={repo_name},
#             navbar=navbar,
#             body=markdown.markdown(md)
#         )
#
#         s3.put_object(Body=rendered_html,
#                       Bucket='gitblog-html',
#                       Key= f'{repo_name}/{filename}.html')