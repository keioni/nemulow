import os
import sys
import pytest

# Ensure the project package can be imported when running tests directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nemulow.utils import (
    convert_markdown_to_html,
    sanitize_filename,
    get_article_list,
    generate_article_html,
    generate_index_html,
)

# テスト用のディレクトリとファイルを設定
TEST_SRC_DIR = 'tests/text/src'
TEST_HTML_DIR = 'tests/text/html'
TEST_TEMPLATE_DIR = 'tests/text/template'
TEST_ARTICLE_TEMPLATE = 'article.html'
TEST_TOP_PAGE_TEMPLATE = 'top_page.html'

@pytest.fixture
def setup_files():
    """テスト用のディレクトリとファイルを作成"""
    os.makedirs(TEST_SRC_DIR, exist_ok=True)
    os.makedirs(TEST_HTML_DIR, exist_ok=True)
    os.makedirs(TEST_TEMPLATE_DIR, exist_ok=True)

    with open(f"{TEST_SRC_DIR}/20210101_Test_Article.md", "w", encoding="utf-8") as f:
        f.write("# Test Article\n\nThis is a test article.")

    with open(f"{TEST_TEMPLATE_DIR}/{TEST_ARTICLE_TEMPLATE}", "w", encoding="utf-8") as f:
        f.write("<html><body>{{ article.content }}</body></html>")

    with open(f"{TEST_TEMPLATE_DIR}/{TEST_TOP_PAGE_TEMPLATE}", "w", encoding="utf-8") as f:
        f.write("<html><body>Top Page</body></html>")

    yield

    # テスト終了後にファイルを削除
    for root, dirs, files in os.walk('tests/text', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def test_convert_markdown_to_html():
    """Markdown から HTML への変換をテスト"""
    content = "# Test Article\n\nThis is a test article."
    result = convert_markdown_to_html(content)
    assert 'content' in result
    assert result['content'] == '<h1>Test Article</h1>\n<p>This is a test article.</p>'

def test_sanitize_filename():
    """ファイル名のサニタイズをテスト"""
    filename = "20210101 Test Article.md"
    sanitized = sanitize_filename(filename)
    assert sanitized == "20210101_Test_Article.md"

def test_get_article_list(setup_files):
    """記事リストの取得をテスト"""
    articles = get_article_list(TEST_SRC_DIR, TEST_HTML_DIR)
    assert len(articles) == 1
    assert articles[0] == "20210101_Test_Article.md"

def test_generate_article_html(setup_files):
    """記事の HTML 生成をテスト"""
    articles = ["20210101_Test_Article.md"]
    generate_article_html(
        articles,
        TEST_SRC_DIR,
        TEST_HTML_DIR,
        f"{TEST_TEMPLATE_DIR}/{TEST_ARTICLE_TEMPLATE}"
    )
    assert os.path.exists(f"{TEST_HTML_DIR}/20210101_Test_Article.html")

def test_generate_index_html(setup_files):
    """インデックス HTML 生成をテスト"""
    generate_index_html(
        TEST_HTML_DIR,
        f"{TEST_TEMPLATE_DIR}/{TEST_TOP_PAGE_TEMPLATE}"
    )
    assert os.path.exists(f"{TEST_HTML_DIR}/index.html")
