"""
Nemulo: A simple static site generator for blogs.
"""

import json
from typing import List

import jinja2
import dotenv

from article import Article


class Nemulow:
    """
    Nemulow: Base category for managing a blog.
    All articles are stored in the `articles` attribute,
    and the all configurations, templates, and the other settings
    are stored in this class.
    """

    config_file: str
    articles: List[Article]
    templates: List[jinja2.Template] = []

    def __init__(self, config_file: str = '.env'):
        """
        Initialize the Nemulow instance with a configuration file.
        """
        self.config_file = config_file
        self.articles = []
        self.config = {}
        self.reload_config(config_file)

    def reload_config(self, config_file: str = '.env'):
        """
        Load the Nemulow configuration.
        """
        dotenv.load_dotenv(config_file)

        self.config = json.load(open(config_file, 'r', encoding='utf-8'))
