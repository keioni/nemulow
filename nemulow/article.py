"""
Convert text to HTML.

This module provides functions to convert one text file to one HTML file.
Specifications for this module are defined in the SPEC.md file.

"""

import os
import re
from typing import List, Optional

from decorate import Decorate


class Article:
    """
    Article class representing a blog article.
    """

    def __init__(self, src_filename: str):
        """
        Initialize the Article instance with a filename.
        """
        self.src_filename = src_filename
        self.dst_filename: str = ''
        self.title: str = ''
        self.metadata: dict = {}
        self.date: str
        self.labels: List[str] = []
        self.summary: Optional[str] = None
        self.card_image: Optional[str] = None
        self.article: List[str] = []
        self.see_more: List[str] = []

    def read(self) -> bool:
        """
        Read the article file and store its raw content.
        """

        # get date and title from the source filename
        # # e.g. 20230101-sample-article.md -> date: 20230101, title: sample-article
        # if date metadata is set in the file, it will override the date from the filename
        match = re.match(r'^(\d{8})-(.*?)\.md$', os.path.basename(self.src_filename))
        if match:
            self.date, self.title = match.groups()
        else:
            return False

        mode = ''
        with open(self.src_filename, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                if line.startswith('# '):
                    mode = 'metadata'
                elif line.startswith('## article'):
                    mode = 'article'
                elif line.startswith('## see more'):
                    mode = 'see more'

                if mode == 'metadata':
                    match = re.match(r'^\* (\w+): (.*)$', line)
                    if match:
                        key, value = match.groups()
                        self.metadata[key] = value
                        if key == 'filename':
                            self.dst_filename = value
                        elif key == 'date':
                            self.date = value
                        elif key == 'summary':
                            self.summary = value
                        elif key == 'card_image':
                            self.card_image = value
                        elif key == 'labels':
                            self.labels = [label.strip() for label in value.split(',')]
                        else:
                            self.metadata[key] = value
                elif mode == 'article':
                    if line and not line.startswith('## '):
                        self.article.append(line)
                elif mode == 'see more':
                    if line and not line.startswith('## '):
                        self.see_more.append(line)

        if not self.labels:
            self.labels = ['Uncategorized']

        # parse date to create date_path
        # e.g. 20230915 -> 2023/0915
        match = re.match(r'^(\d{4})(\d{4})$', self.date)
        date_path = ''
        if match:
            date_path = match.group(1) + '/' + match.group(2)

        # set destination filename
        # for example, if date is 20230101 and destination filename is output-sample-article
        # then the destination filename will be 2023/0101/output-sample-article.html
        if not self.dst_filename:
            # if filename metadata is not set, use the title from the filename
            # highly recommended to set filename metadata
            self.dst_filename = self.title

        self.dst_filename = (
            os.environ.get('DEST_PATH', '.') + '/' +
            date_path + '-' +
            self.dst_filename + '.html'
        )

        return True

    def check_modified(self) -> bool:
        """
        Check if the article has been modified.
        """
        if os.path.exists(self.dst_filename):
            if os.path.getmtime(self.dst_filename) < os.path.getmtime(self.src_filename):
                return True
        return False

    def _paragraphize(self, lines: List[str]) -> List[str]:
        """
        lines to paragraphs.
        blank lines are treated as paragraph breaks.
        """

        paragraphs = []
        tmp_paragraph = []

        for line in lines:
            line = line.strip()
            if not line:
                if tmp_paragraph:
                    paragraphs.append('\n'.join(tmp_paragraph))
                    tmp_paragraph = []
            else:
                tmp_paragraph.append(line)

        if tmp_paragraph:
            paragraphs.append('\n'.join(tmp_paragraph))

        for paragraph in paragraphs:
            if not paragraph:
                continue
            if paragraph.startswith('>><<'):
                paragraph = paragraph[4:].strip()
                paragraph = f'<p style="text-align: center;">{paragraph}</p>'
            elif paragraph.startswith('>>>>'):
                paragraph = paragraph[4:].strip()
                paragraph = f'<p style="text-align: right;">{paragraph}</p>'
            elif paragraph == '---':
                paragraph = '<hr>'
            elif paragraph.startswith('"""') and paragraph.endswith('"""'):
                paragraph = paragraph[3:-3].strip()
                paragraph = f'<blockquote>{paragraph}</blockquote>'
            else:
                paragraph = f'<p>{paragraph}</p>'
            paragraph = re.sub(r'\n+', '<br>\n', paragraph)

        return paragraphs

    def _remove_comments(self, content: str) -> str:
        """
        Remove comments from the string.
        """
        return re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    def _remove_tags(self, content: str) -> str:
        """
        Remove HTML tags from the string.
        """
        return re.sub(r'<.*?>', '', content, flags=re.DOTALL)

    def _decorate(self, content: str) -> str:
        """
        Decorate markdown-like syntax in the string.
        see SPEC.md for details.
        """
        content = Decorate().decorate(content)
        return content
