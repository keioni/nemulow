"""
Nemulo: A simple static site generator for blogs.
"""

import os
import re

from jinja2 import Template

from article import Article, ArticleList

# Constants
TEXT_SRC_DIR = 'text/src'
TEXT_HTML_DIR = 'text/html'
TEMPLATE_DIR = 'text/template'
TOP_PAGE_TEMPLATE = 'top_page.html'
ARTICLE_TEMPLATE = 'article.html'
JS_TEMPLATE = 'articles.js'
JS_OUTPUT = 'text/html/articles.js'
ARTICLE_COUNT = 5
SIDEBAR_COUNT = 20


def main():
    """Main function."""
    if not os.path.exists(TEXT_HTML_DIR):
        os.makedirs(TEXT_HTML_DIR)

    ArticleList.load_articles(TEXT_SRC_DIR)
