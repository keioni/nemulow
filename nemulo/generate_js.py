
JS_TEMPLATE = 'articles.js'
JS_OUTPUT = 'text/html/articles.js'

def generate_java_script(articles: list[dict]):
    """Generate JavaScript code to render articles in the sidebar."""
    js = 'const articles = ['
    for article in articles:
        js += '{'
        js += f'title: "{article["Title"][0]}",'
        js += f'category: "{article["Category"][0]}",'
        js += f'summary: "{article["Summary"][0]}",'
        js += f'date: "{article["Date"][0]}",'
        js += f'content: `{article["content"]}`'
        js += '},'
    js += '];'
    with open(JS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(js)

