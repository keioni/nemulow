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

        # original syntax (heading levels)
        # Note: H1 (# ) is reserved for signature.
        # H2 (## ) is used for "article" and "See more" section, so not processed here.
        content = re.sub(r'^#### +(.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^### +(.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)

        return content
