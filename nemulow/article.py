"""
Convert text to HTML.

This module provides functions to convert one text file to one HTML file.
Specifications for this module are defined in the SPEC.md file.

"""

import os
import re
from datetime import date

from typing import List, Optional


class Article:
    """
    Article class representing a blog article.
    """

    def __init__(self, filename: str):
        """
        Initialize the Article instance with a filename.
        """
        self.src_filename = filename
        self.dst_filename: str = ''
        self.dst_file_path: str = ''
        self._raw_content: List[str] = []
        self.title: str = ''
        self.metadata: dict = {}
        self.date: Optional[str] = None
        self.category: Optional[str] = 'uncategorized'
        self.summary: List[str] = []
        self.card_image: str = ''
        self.article: List[str] = []
        self.see_more: List[str] = []

    def read(self) -> None:
        """
        Read the article file and store its raw content.
        """
        mode = ''
        with open(self.src_filename, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                if line.startswith('# '):
                    mode = 'metadata'
                elif line.startswith('## summary'):
                    mode = 'summary'
                elif line.startswith('## article'):
                    mode = 'article'
                elif line.startswith('## see more'):
                    mode = 'see more'

                if mode == 'metadata':
                    match = re.match(r'^\* (\w+): (.*)$', line)
                    if match:
                        key, value = match.groups()
                        self.metadata[key] = value
                        if key == 'title':
                            self.title = value
                        elif key == 'filename':
                            self.filename = value
                        elif key == 'date':
                            self.date = value
                elif mode == 'summary':
                    if line and not line.startswith('## '):
                        self.summary.append(line)
                elif mode == 'article':
                    if line and not line.startswith('## '):
                        self.article.append(line)
                elif mode == 'see more':
                    if line and not line.startswith('## '):
                        self.see_more.append(line)

        # if date metadata is not set, use today's date
        if not self.date:
            self.date = date.today().strftime('%Y%m%d')

        # get destination filename
        self.dst_file_path = (
            os.environ.get('DEST_PATH', '.') + '/' +
            self.date + '-' +
            self.dst_filename + '.html'
        )

    def check_modified(self) -> bool:
        """
        Check if the article has been modified.
        """

        # get destination filename and that file's mtime
        if os.path.exists(self.dst_filename):
            if os.path.getmtime(self.dst_filename) < os.path.getmtime(self.src_filename):
                return True

        # when newer than dst file, update dst file
        return False

    def make_summary(self) -> str:
        """
        Make the summary HTML.
        """
        summary = self._paragraphize(self.summary, remove_tag=True)
        summary = self._remove_comments(summary)
        summary = self._remove_tags(summary)

        return summary

    def make_article(self) -> str:
        """
        Make the article HTML.
        """
        article = self._paragraphize(self.article)
        article = self._remove_comments(article)
        article = self._decorate(article)

        return article

    def _paragraphize(self, lines: List[str], remove_tag: bool = False) -> str:
        """
        Convert lines into html paragraphs.
        blank lines are treated as paragraph breaks.
        """

        stripped_lines = []

        for line in lines:
            line = line.strip()
            if line:
                stripped_lines.append(line)

        if remove_tag:
            combined_string = '\n'.join(stripped_lines)
            combined_string = combined_string.strip()
            combined_string = re.sub(r'<.*?>', '', combined_string)
        else:
            combined_string = '<br>\n'.join(stripped_lines)
            combined_string = combined_string.strip()
            combined_string = re.sub(r'<br><br>', '</p>\n\n<p>', combined_string)
            combined_string = '<p>' + combined_string + '</p>'

        return combined_string

    def _remove_comments(self, content: str) -> str:
        """
        Remove comments from the string.
        This string was combined from multiple lines.
        Comments are enclosed in <!-- and -->.
        """
        return re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    def _remove_tags(self, content: str) -> str:
        """
        Remove HTML tags from the string.
        """
        return re.sub(r'<.*?>', '', content)

    def _decorate(self, content: str) -> str:
        """
        Decorate markdown-like syntax in the string.
        see SPEC.md for details.
        """
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        return content
