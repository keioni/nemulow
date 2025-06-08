"""
Nemulo: A simple static site generator for blogs.
"""

import json
import os
from typing import List, Union

from article import Article, ArticleList


class Blog:
    """
    Base category for managing a blog.
    """
    config_file: str = 'config.json'
    config: dict[str, Union[str, int, bool]] = {}
    articles: List[Article]

    def __init__(self, config_file: str = 'config.json'):
        self.config = json.load(open(config_file, 'r', encoding='utf-8'))

    def reload_config(self, config_file: str):
        """
        Load the blog configuration.
        """
        self.config = json.load(open(config_file, 'r', encoding='utf-8'))

    def build(self):
        """
        Build the blog by processing articles and applying configuration.
        """
        if not self.config:
            raise ValueError("Configuration is not set.")


class Configure:
    """
    Class for managing blog configuration.
    """
    dest_path: str
    src_path: str
    template_path: str

    def __init__(self):
        """
        Initialize the configuration with default paths.
        """
        self.dest_path = ''
        self.src_path = ''
        self.template_path = ''

    def load_config_file(self, config_file: str):
        """
        Load configuration from a file.
        """
        # Placeholder for loading logic
        pass
        # Load articles from the source directory


class Template:
    """
    Class for managing blog templates.
    """
    def __init__(self, template_path: str):
        self.template_path = template_path

    def load_template(self, template_name: str):
        """
        Load a template file.
        """
        with open(f"{self.template_path}/{template_name}", "r", encoding="utf-8") as f:
            return f.read()
