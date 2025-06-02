"""
Convert text to HTML.

This module provides functions to convert text to HTML.
Specifications for this module are defined in the SPEC.md file.

"""

import re

from datetime import datetime
from typing import TypedDict, List, Optional

class ArticleList:
    """
    Class representing a list of articles.
    """
    def __init__(self):
        """
        Initialize the article list.
        """
        self.articles = []

    def add(self, article):
        """
        Add an article to the list.
        """
        self.articles.append(article)

    def get(self):
        """
        Get the list of articles.
        """
        return self.articles


class Metadata(TypedDict):
    """
    TypedDict for Article metadata.
    """
    title: str
    timestamp: datetime
    category: Optional[str]
    tags: Optional[List[str]]


class Article:
    """
    Class representing an article.
    """
    filename: str
    raw_content = []
    content = ''
    metadata: Metadata = {
        'title': '',
        'timestamp': None,
        'category': 'uncategorized',
        'tags': [],
    }
    first_part: List[str] = []
    last_part: List[str] = []

    def __init__(self, filename: str):
        """
        Initialize the article object.
        """
        self.filename = filename

    def open(self):
        """
        Open the article file and read its content.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                self.raw_content.append(line.strip())

    def read(self):
        """
        Read the article content and metadata.
        """
        self._read_metadata()
        self._remove_comments()
        self._read_content()

    def _read_metadata(self):
        """
        read metadata are defined in the first lines of the file.

        metadata keys are:
        - 'title', 'timestamp', 'category', and 'tags'.

        metadata are defined in the following format:
        name (key) and value are separated by at least one space and tab.
        for example:
        title I am a cat
        timestamp 2025/04/03 12:00
        category cat
        tags cat, animal, pet

        timestamp is in ISO format.
        (timestamp.isoformat() is used to convert the timestamp to ISO format)
        category is optional.
        tags are optional.

        metadata is read until an empty line is found.
        """
        for line in self.raw_content:
            # Read the first line of the file
            line = line.strip()
            if not line:
                break
            key, value = line.split(maxsplit=1)
            if key == 'title':
                self.metadata['title'] = value
            elif key == 'timestamp':
                try:
                    self.metadata['timestamp'] = datetime.fromisoformat(value)
                except ValueError:
                    self.metadata['timestamp'] = datetime.strptime(value, '%Y/%m/%d %H:%M')
            elif key == 'tags':
                self.metadata['tags'] = [tag.strip() for tag in value.split(',')]
            elif key == 'category':
                self.metadata['category'] = value

    def _remove_comments(self):
        """
        remove comments from the line.
        comments are defined by <!-- and --> tags like HTML.
        multiline comments are supported.
        """
        in_comment = False
        remove_commented_lines = []

        # remove comments
        for line in self.raw_content:
            if '<!--' in line:
                if '-->' in line:
                    line = re.sub(r'<!--.*-->', '', line)
                else:
                    line = re.sub(r'<!--.*', '', line)
                    in_comment = True
                remove_commented_lines.append(line)
                continue
            if in_comment:
                if '-->' in line:
                    in_comment = False
                    line = re.sub(r'.*-->', '', line)
                else:
                    line = ''
            remove_commented_lines.append(line)
        self.raw_content = remove_commented_lines

    def _read_content(self):
        """
        Parse the article content and convert it to HTML.
        """

        # Decorate the raw content with HTML tags like markdown
        raw_content = self._decorate_content(self.raw_content)
        # Parse the article content and convert it to HTML.
        paragraphs = self._parse_paragraph(raw_content)
        # Align the paragraphs based on the alignment syntax
        paragraphs = self._align_paragraphs(paragraphs)

    def _decorate_content(self, raw_content: List[str]) -> List[str]:
        """
        Decorate the raw content with HTML tags.
        Some markdown syntax is supported.

        The following markdwon syntax is supported:
        - **string** : bold
        - `code` : code
        - [alt text](url) : link
        - ![alt text](url) : image

        Followings are original syntax:
        - ^^^string^^^ : emphasis text by css "text-emphasis-style: dot"
        - ^^type^^string^^^ : same as above but with a custom (type) emphasis style
        - ~~string~~ : strikethrough
        - ||string||ruby string|| : ruby
        """
        decorated_content = [
            re.sub(r'\|\|(.+?)\|\|(.+?)\|\|', r'<ruby>\1<rp>\(<rt>\2</rt><rp>\)</rp></ruby>',
            re.sub(r'~~(.*?)~~', r'<del>\1</del>',
            re.sub(r'\^\^(.+?)\^\^\(.+?)\^\^', r'<span class="text-emphasis-style: \1">\2</span>',
            re.sub(r'\^\^\^(.*?)\^\^\^', r'<span class="text-emphasis-style: dot">\1</span>',
            re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">',
            re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>',
            re.sub(r'`(.*?)`', r'<code>\1</code>',
            re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line))))))))
            for line in raw_content
        ]
        return decorated_content

    def _parse_paragraph(self, raw_content: List[str]) -> List[str]:
        """
        Parse a paragraph from the raw content.
        """
        paragraphs: List[str] = []
        current_paragraph: List[str] = []

        # Parse Paragraph
        for line in raw_content:
            # Note: lines in raw_content are already stripped of leading and trailing whitespace
            if not line:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = []
            else:
                if line.startswith('>>>'): # start of blockquote
                    paragraphs.append(['<blockquote>'])
                elif line.startswith('<<<'): # end of blockquote
                    current_paragraph.append(['<blockquote>'])
                elif line.startswith('---'):  # horizontal rule
                    paragraphs.append(['<hr>'])
                else:
                    current_paragraph.append(line.strip())

        # add the last paragraph if it exists
        if current_paragraph:
            paragraphs.append(current_paragraph)

        # convert paragraphs to HTML
        html_paragraphs = [
            f'<p>{"<br>".join(paragraph)}</p>' for paragraph in paragraphs
        ]
        return html_paragraphs

    def _align_paragraphs(self, html_paragraphs: List[str]) -> List[str]:
        """
        Align paragraphs based on the alignment syntax.
        <p>=< : left aligned
        <p>=| : center aligned
        <p>=> : right aligned
        """
        aligned_paragraphs = []

        for paragraph in html_paragraphs:
            if paragraph.startswith('<p>='):
                if paragraph.startswith('<p>=>'):
                    paragraph = paragraph.replace('<p>=>', '<p class="right">')
                elif paragraph.startswith('<p>=|'):
                    paragraph = paragraph.replace('<p>=|', '<p class="center">')
                elif paragraph.startswith('<p>=<'):
                    # default is left aligned
                    paragraph = paragraph.replace('<p>=<', '<p>')
            aligned_paragraphs.append(paragraph)

        return aligned_paragraphs

    def _divide_parts(self, paragraphs: List[str]) -> List[str]:
        """
        Divide the article into parts.
        """
        in_first_part = True

        for paragraph in paragraphs:
            if paragraph.startswith('<p>:break'):
                if in_first_part:
                    in_first_part = False
                    continue
            else:
                if in_first_part:
                    self.first_part.append(paragraph)
                else:
                    self.last_part.append(paragraph)
        return self.first_part + self.last_part
