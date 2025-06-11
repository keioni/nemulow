"""
Nemulo: A simple static site generator for blogs.
"""

import json
import os
from typing import List, Union

import jinja2
import yaml

from article import Article


class Nemulow:
    """
    Nemulow: Base category for managing a blog.
    All articles are stored in the `articles` attribute,
    and the all configurations, templates, and the other settings
    are stored in this class.
    """

    config_file: str = 'config.json'
    config: dict[str, Union[str, int, bool]] = {}
    articles: List[Article]
    templates: List[jinja2.Template] = []

    def __init__(self, config_file: str = 'config.json'):
        self.config = json.load(open(config_file, 'r', encoding='utf-8'))

    def reload_config(self, config_file: str):
        """
        Load the Nemulow configuration.
        """
        self.config = json.load(open(config_file, 'r', encoding='utf-8'))

    def build(self):
        """
        Build the Nemulow site by processing articles and applying configuration.
        """
        if not self.config:
            raise ValueError("Configuration is not set.")


class Configure:
    """
    Class for managing Nemulow configuration.
    """
    dest_path: str
    src_path: str
    template_path: str
    templates: list

    def __init__(self):
        """
        Initialize the configuration with default paths.
        """
        self.all_config = {}
        self.dest_path = ''
        self.src_path = ''
        self.template_path = ''
        self.templates = []

    def load_config_file(self, config_file: str):
        """
        Load configuration from a file.
        """
        # Placeholder for loading logic
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        with open(config_file, 'r', encoding='utf-8') as file:
            self.all_config = json.load(file)
            self.dest_path = self.all_config.get('dest_path', './html')
            self.src_path = self.all_config.get('src_path', './text')
            self.template_path = self.all_config.get('template_path', './templates')

    def load_templates(self):
        """
        Load all templates from the template path.
        """
        for template_file in os.listdir(self.template_path):
            if template_file.endswith(".j2"):
                template = Template(os.path.join(self.template_path, template_file))
                self.templates.append(template)

class Template:
    """
    Class for managing blog templates.
    """
    template_path: str
    template_name: str = ''
    template_body: str = ''

    def __init__(self, template_path: str = 'templates'):
        self.template_path = template_path

    def load_template(self, template_name: str):
        """
        Load a template file.
        """
        template_file = os.path.join(self.template_path, template_name)
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template file '{template_file}' not found.")
        with open(template_file, 'r', encoding='utf-8') as file:
            self.template_body = file.read()

    def render_template(self, context: dict):
        """
        Render a template with the given context.
        """
        template = jinja2.Template(self.template_body)
        return template.render(context)
