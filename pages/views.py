from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def home(request):

    git_code = '''
$ git clone git@github.com:your-github-username/your-gitblog.git
$ echo '# My first Gitblog post' > public/hello-world.md
$ git add public/hello-world.md
$ git commit -m 'my first post'
$ git push
'''

    return render(request, 'pages/home.html', context={
        'git_code_html': highlight(git_code, get_lexer_by_name('console'), HtmlFormatter()),
        'git_code_styles': (
            HtmlFormatter(style='solarized-light').get_style_defs('html:not(.dark) .highlight'),
            HtmlFormatter(style='solarized-dark').get_style_defs('html.dark .highlight'), )
    })


def auth_logout(request):

    user = request.user

    logout(request)
    return HttpResponseRedirect(user.blog_set.first().get_absolute_url())
