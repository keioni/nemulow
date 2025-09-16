"""
A module to decorate article content with HTML structure.
"""

import re


class Decorate:
    def __init__(self):
        pass

    def decorate(self, content: str) -> str:
        """
        Decorate the article content with HTML structure.
        Supports markdown-like syntax and some original syntax.
        See SPEC.md for details.
        """

        # markdown-like syntax
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
        content = re.sub(r'~~(.*?)~~', r'<del>\1</del>', content)
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', content)
        content = re.sub(r'^---+$', r'<hr>', content, flags=re.MULTILINE)

        # original syntax (heading levels)
        # Note: H1 (# ) is reserved for the article title, so not processed here.
        # H2 (## ) is used for "Article" and "See more" section, so not processed here.
        content = re.sub(r'^#### +(.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^### +(.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)

        # original syntax (blockquotes)
        # content string was combined from multiple lines with <p> and <br>
        # so we need to handle that.
        # if '<p>>>' in content or '<br>>>' in content:
        #     content = re.sub(r'<(p|br>\>\>\>(.*?)<\/p>', r'<p style="text-align: right;">\1</p>', content, flags=re.DOTALL)
        # content = re.sub(r'<p>```<br>(.*?)<br>```<\/p>', r'<blockquote>\1</blockquote>', content, flags=re.DOTALL)
        # content = re.sub(r'<p>\>\>\>(.*?)<<<<\/p>', r'<p style="text-align: center;">\1</p>', content, flags=re.DOTALL)
        # content = re.sub(r'<p>\>\>\>(.*?)<\/p>', r'<p style="text-align: right;">\1</p>', content, flags=re.DOTALL)

        def replace_blockquote(match):
            inner_content = match.group(1).strip()
            inner_content = re.sub(r'^<p>', '', inner_content)
            inner_content = re.sub(r'<br>\s*$', '', inner_content)
            return f'<blockquote>{inner_content}</blockquote>'

        content = re.sub(r'^> +(.*?)$', replace_blockquote, content, flags=re.MULTILINE)
        content = re.sub(r'^>+$', r'</blockquote>', content, flags=re.MULTILINE)

        return content
