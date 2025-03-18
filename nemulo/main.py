"""
Nemulo: A simple static site generator for blogs.
"""

import os
import re

from jinja2 import Template

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

def convert_markdown_to_html(content: str) -> dict:
    """Convert Markdown content to HTML."""
    md = markdown.Markdown(extensions=['meta'])
    html_content = md.convert(content)
    metadata = md.Meta if hasattr(md, "Meta") else {}  # Prevent AttributeError
    metadata['content'] = html_content
    return metadata

def sanitize_filename(filename: str) -> str:
    """Replace spaces and unsafe characters with underscores."""
    return re.sub(r'[\\/*?:"<>| ]', '_', filename)

def get_article_list(src_path: str, dst_path: str) -> list[str]:
    """Get a list of article files that need to be updated."""
    all_md_files = os.listdir(src_path)

    updated_md_files = []
    for md_file in all_md_files:
        if not md_file.endswith(".md"):
            continue

        md_mtime = os.path.getmtime(f"{src_path}/{md_file}")

        html_file = sanitize_filename(os.path.splitext(md_file)[0] + ".html")
        html_path = f"{dst_path}/{html_file}"
        html_mtime = os.path.getmtime(html_path) if os.path.exists(html_path) else 0

        # Update the HTML file if the Markdown file is newer
        # (If the HTML file is missing, html_mtime is 0, making the condition always true.)
        if md_mtime > html_mtime:
            updated_md_files.append(md_file)

    return updated_md_files


def generate_article_html(
    articles: list[dict],
    src_path: str,
    dst_path: str,
    template: str
) -> None:
    """Generate HTML files from Markdown files."""
    with open(template, "r", encoding="utf-8") as f:
        article_template = Template(f.read())

    for md_file in articles:
        html_file = sanitize_filename(os.path.splitext(md_file)[0] + ".html")
        html_path = f"{dst_path}/{html_file}"
        with open(f"{src_path}/{md_file}", "r", encoding="utf-8") as f:
            content = f.read()

        md_data = convert_markdown_to_html(content)
        html = article_template.render(article=md_data)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

def generate_index_html(dst_path: str, template: str) -> None:
    """Generate HTML files from Markdown files."""
    with open(template, "r", encoding="utf-8") as f:
        top_page_template = Template(f.read())

    for html_file in os.listdir(dst_path).sort:
        if html_file == "index.html":
            continue
        if not html_file.endswith(".html"):
            continue
        with open(f"{dst_path}/{html_file}", "r", encoding="utf-8") as f:
            content = f.read()

    # html = top_page_template.render(article=latest_article)
    # with open(f"{dst_path}/index.html", "w", encoding="utf-8") as f:
    #     f.write(html)

def main():
    """Main function."""
    if not os.path.exists(TEXT_HTML_DIR):
        os.makedirs(TEXT_HTML_DIR)

    articles = get_article_list(TEXT_SRC_DIR, TEXT_HTML_DIR)
    generate_article_html(
        articles,
        TEXT_SRC_DIR,
        TEXT_HTML_DIR,
        f"{TEMPLATE_DIR}/{ARTICLE_TEMPLATE}"
    )
    generate_index_html(
        TEXT_HTML_DIR,
        f"{TEMPLATE_DIR}/{TOP_PAGE_TEMPLATE}"
    )
