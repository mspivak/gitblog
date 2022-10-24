from typing import Tuple

import html
import misaka
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


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
        self.extracted_files = []
        super(SyncRenderer, self).__init__(**kwargs)

    def image(self, raw_url, title='', alt=''):
        if not raw_url.startswith('http'):
            file, created = self.blog.file_set.get_or_create(
                repo_path=raw_url,
                defaults={'alt': alt, 'title': title})
            self.extracted_files.append(file)
            return super().image(file.url, file.title, file.alt)
        else:
            return super().image(raw_url, title, alt)


def md_to_html_and_css(post) -> Tuple[str, Tuple[str, str]]:

    renderer = GitblogRenderer(blog=post.blog)

    to_html = misaka.Markdown(renderer, extensions=('tables', 'fenced-code', 'footnotes', 'autolink', 'strikethrough',
                                                    'underline', 'highlight', 'quote', 'superscript',
                                                    'math', 'math-explicit', ))

    return to_html(post.content_md), \
           (HtmlFormatter(style='solarized-light').get_style_defs('html:not(.dark) .highlight'), HtmlFormatter(style='solarized-dark').get_style_defs('html.dark .highlight'), )
