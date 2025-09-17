"""
Convert text to HTML.

This module provides functions to convert one text file to one HTML file.
Specifications for this module are defined in the SPEC.md file.

"""

import os
import re
from typing import List

from decorate import Decorate


class Article:
    """
    Article class representing a blog article.
    """

    def __init__(self, src_filename: str):
        """
        Initialize the Article instance with a filename.
        """
        self.src_filename: str = src_filename
        self.title: str = ''
        self.date: str = ''
        self.metadata: dict = {
            'filename': '',
            'updated_at': '',
            'summary': None,
            'card_image': None,
            'labels': '',
        }
        self.article: List[str] = []
        self.see_more: List[str] = []

    def read(self) -> bool:
        """
        Read the article file and store its raw content.
        """

        # get date and title from the source filename
        # e.g. 20230101-sample-article.md -> date: 20230101, title: sample-article
        match = re.match(r'^(\d{8})-(.*?)\.md$', os.path.basename(self.src_filename))
        if match:
            self.date, self.title = match.groups()
            match = re.match(r'^(\d{4})(\d{2})(\d{2})$', self.date)
            if match:
                # used for destination filename
                year, month, day = match.groups()
            else:
                return False
        else:
            return False

        mode = ''
        with open(self.src_filename, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.rstrip('\n')
                if line.startswith('# '):
                    mode = 'metadata'
                    continue
                elif line.startswith('## article'):
                    mode = 'article'
                    continue
                elif line.startswith('## see more'):
                    mode = 'see more'
                    continue

                if mode == 'metadata':
                    match = re.match(r'^\* (\w+): (.*)$', line)
                    if match:
                        key, value = match.groups()
                        self.metadata[key] = value
                elif mode == 'article':
                    self.article.append(line)
                elif mode == 'see more':
                    self.see_more.append(line)

        # set destination filename
        # for example, if date is 20230101 and title is output-sample-article
        # then the destination filename will be 2023/0101-output-sample-article.html
        # if filename metadata is not set, use the title from the source filename.
        # HIGHLY recommended to set "filename" metadata.
        self.title = self.metadata.get('filename', self.title)
        self.dst_filename = (
            os.environ.get('DEST_PATH', '.') +
            f'/{year}/{month}{day}-{self.title}.html'
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
        return Decorate().decorate(content)
