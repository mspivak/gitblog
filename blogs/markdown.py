from typing import Tuple

import houdini
import misaka
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


class HighlighterRenderer(misaka.HtmlRenderer):

    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = guess_lexer(text)

        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

        return '\n<pre><code>{}</code></pre>\n'.format(houdini.escape_html(text.strip()))


def md_to_html_and_css(content_md: str) -> Tuple[str, str]:

    renderer = HighlighterRenderer()

    to_html = misaka.Markdown(renderer, extensions=('tables', 'fenced-code', 'footnotes', 'autolink', 'strikethrough',
                                                    'underline', 'highlight', 'quote', 'superscript',
                                                    'math', 'math-explicit', ))

    return to_html(str(content_md)), HtmlFormatter(style='solarized-dark').get_style_defs('.highlight')
