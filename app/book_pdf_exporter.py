# app/book_pdf_exporter.py
from weasyprint import HTML
from jinja2 import Template
import os

def save_book_as_pdf(title: str, content: str, filename: str = "star_wars_book.pdf") -> str:
    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{{ title }}</title>
        <style>
            body {
                font-family: Georgia, serif;
                margin: 50px;
                line-height: 1.6;
            }
            h1, h2 {
                color: #333;
                text-align: center;
            }
            h2 {
                margin-top: 40px;
            }
            p {
                margin: 10px 0;
                text-align: justify;
            }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        {% for section in sections %}
            <h2>{{ section.heading }}</h2>
            {% for para in section.body %}
                <p>{{ para }}</p>
            {% endfor %}
        {% endfor %}
    </body>
    </html>
    """)

    sections = []
    if "## " in content:
        for sec in content.split("## "):
            if not sec.strip():
                continue
            lines = sec.strip().split("\n", 1)
            heading = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            paragraphs = [p.strip() for p in body.split("\n") if p.strip()]
            sections.append({"heading": heading, "body": paragraphs})
    else:
        paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
        sections.append({"heading": "Story", "body": paragraphs})

    html_content = html_template.render(title=title, sections=sections)

    os.makedirs("generated_books", exist_ok=True)
    output_path = os.path.join("generated_books", filename)
    HTML(string=html_content).write_pdf(output_path)

    return output_path
