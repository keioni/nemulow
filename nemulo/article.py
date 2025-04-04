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
    tags: List[str]

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

    def _decorate(self, raw_content: List[str]) -> List[str]:
        """
        Decorate the raw content with HTML tags like markdown.
        This function converts the raw content to HTML.

        The following syntax is supported:
        - **string** : bold
        - `code` : code
        - [alt text](url) : link
        - ![alt text](url) : image
        """
        decorated_content = [
            re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">',
            re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>',
            re.sub(r'`(.*?)`', r'<code>\1</code>',
            re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line))))
            for line in raw_content
        ]
        return decorated_content


    def _remove_comments(self, raw_content: List[str]) -> list:
        """
        Remove comments from the line.
        Comments are defined by <!-- and --> tags like HTML.
        Multiline comments are supported.
        """
        in_comment = False
        remove_commented_lines = []

        for line in raw_content:
            line = line.strip()

            if re.search(r'<!-- ', line):
                if re.search(r' -->', line):
                    line = re.sub(r'\s*<!--.*?-->', '', line)
                else:
                    line = re.sub(r'\s*<!--.*', '', line)
            if in_comment:
                if re.search(r'-->', line):
                    in_comment = False
                    line = re.sub(r'.*?-->', '', line)
                    in_comment = True
            remove_commented_lines.append(line)

        return remove_commented_lines

    def _parse_pragraph(self, raw_content: List[str]) -> List[str]:
        """
        Parse a paragraph from the raw content.
        """
        paragraphs: List[str] = []
        current_paragraph: List[str] = []

        # Parse Paragraph
        for line in raw_content:
            # remove leading and trailing whitespace
            line = line.strip()

            # if line is empty, add the current paragraph to the list
            if not line:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = []
            elif line.startswith('>>>'):
                paragraphs.append(['<blockquote>'])
            elif line.startswith('<<<'):
                current_paragraph.append(['<blockquote>'])
            elif line.startswith('---'):  # Horizontal rule
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

    def read(self):
        """
        read the article file and parse the metadata.
        metadata are defined in the first lines of the file.

        metadata kinds and format:
        
        title article title
        timestamp 2025/04/03
        tags tag1,tag2,tag3
        
        timestamp format are:
        - YYYY/MM/DD HH:mm
        - any string that can be parsed by timestamp.fromisoformat
        
        name (key) and value are separated by at least one space and tab.
        metadata is read until an empty line is found.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
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
            # Read the rest of the file
            self.raw_content = file.readlines()

    def parse(self):
        """
        Parse the article content and convert it to HTML.
        """

        # decorate the raw content with HTML tags
        # like markdown
        raw_content = self._decorate(self.raw_content)

        # remove comments from the raw content
        # and remove leading and trailing whitespace
        raw_content = self._remove_comments(raw_content)

        # parse the article content and convert it to HTML.
        paragraphs = self._parse_pragraph(self.raw_content)
