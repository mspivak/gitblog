from typing import Tuple

import urllib.request
import html
import misaka
import boto3
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

from django.conf import settings

# from .models import Blog, File


class GitblogRenderer(misaka.HtmlRenderer):

    def __init__(self, blog, flags=(), nesting_level=0):
        self.blog = blog
        super(GitblogRenderer, self).__init__(flags, nesting_level)

    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = guess_lexer(text)

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

        return '\n<pre><code>{}</code></pre>\n'.format(html.escape(text.strip()))

    def image(self, raw_url, title='', alt=''):

        if not raw_url.startswith('http'):

            file = self.blog.file_set.get(repo_path=raw_url)
            url = file.url
            alt = file.alt
            title = file.title

        else:
            url = misaka.api.escape_html(raw_url)

        maybe_alt = ' alt="%s"' % misaka.api.escape_html(alt) if alt else ''
        maybe_title = ' title="%s"' % misaka.api.escape_html(title) if title else ''

        return f'<img src="{url}"{maybe_alt}{maybe_title} />'


class SyncRenderer(GitblogRenderer):
    """
    This renderer is used exclusively to crawl a post markdown,
    extract all images, upload them to s3 and create a file on database.
    """

    def __init__(self, **kwargs):
        super(SyncRenderer, self).__init__(**kwargs)

    extracted_files = []

    def image(self, raw_url, title='', alt=''):

        if not raw_url.startswith('http'):

            object_key = f'{self.blog.owner.username}/{self.blog.slug}/{raw_url}'

            file, created = self.blog.file_set.get_or_create(repo_path=raw_url, defaults={
                'url': f'https://{settings.AWS_USER_FILES_BUCKET_NAME}.s3.amazonaws.com/{object_key}',
                'alt': alt,
                'title': title
            })

            if created:

                print(f'Downloading {file} from Github')
                github_file = self.blog.get_github_repo().get_contents(raw_url)

                if github_file.content:
                    content = github_file.decoded_content
                else:
                    # file size is over 1MB
                    with urllib.request.urlopen(github_file.download_url) as raw_file:
                        content = raw_file.read()

                print(f'Uploading {file} from to s3://{settings.AWS_USER_FILES_BUCKET_NAME}/{object_key}')
                boto3.client('s3').put_object(
                    Body=content,
                    Bucket=settings.AWS_USER_FILES_BUCKET_NAME,
                    Key=object_key
                )

            self.extracted_files = file

            return super().image(file.url, file.title, file.alt)

        else:

            return super().image(raw_url, title, alt)


def md_to_html_and_css(post) -> Tuple[str, str]:

    renderer = GitblogRenderer(blog=post.blog)

    to_html = misaka.Markdown(renderer, extensions=('tables', 'fenced-code', 'footnotes', 'autolink', 'strikethrough',
                                                    'underline', 'highlight', 'quote', 'superscript',
                                                    'math', 'math-explicit', ))

    return to_html(post.content_md), HtmlFormatter(style='solarized-dark').get_style_defs('.highlight')
