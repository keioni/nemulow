import os
from pathlib import Path
from typing import List, Dict

import markdown
from jinja2 import Environment, FileSystemLoader


def convert_markdown_to_html(content: str) -> Dict[str, str]:
    """Convert markdown text to HTML."""
    html = markdown.markdown(content)
    return {"content": html}


def sanitize_filename(filename: str) -> str:
    """Return a safe filename for generated HTML."""
    return filename.replace(" ", "_")


def get_article_list(src_dir: str, html_dir: str) -> List[str]:
    """Return list of article filenames to process."""
    articles = []
    for entry in os.listdir(src_dir):
        if entry.lower().endswith(".md"):
            sanitized = sanitize_filename(entry)
            articles.append(sanitized)
    return articles


def generate_article_html(articles: List[str], src_dir: str, html_dir: str, template_path: str) -> None:
    """Generate HTML files for each article."""
    env = Environment(loader=FileSystemLoader(Path(template_path).parent))
    tmpl = env.get_template(Path(template_path).name)
    os.makedirs(html_dir, exist_ok=True)

    for article in articles:
        src_file = Path(src_dir) / article
        # In case sanitize_filename changed the name
        if not src_file.exists():
            src_file = Path(src_dir) / article.replace("_", " ")
        with open(src_file, "r", encoding="utf-8") as f:
            content = f.read()
        html_body = convert_markdown_to_html(content)["content"]
        rendered = tmpl.render(article={"content": html_body})
        out_file = Path(html_dir) / (Path(article).stem + ".html")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(rendered)


def generate_index_html(html_dir: str, template_path: str) -> None:
    """Generate index.html."""
    env = Environment(loader=FileSystemLoader(Path(template_path).parent))
    tmpl = env.get_template(Path(template_path).name)
    os.makedirs(html_dir, exist_ok=True)
    out_path = Path(html_dir) / "index.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(tmpl.render())
