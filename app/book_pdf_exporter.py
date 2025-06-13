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
            @page {
                margin: 50px 70px;
                @bottom-center {
                    content: counter(page);
                    font-size: 12px;
                    font-family: Georgia, serif;
                }
            }
            @page:first {
                @bottom-center {
                    content: "";
                }
            }

            body {
                font-family: Georgia, serif;
                line-height: 1.7;
                margin: 0;
                padding: 0;
                text-align: justify;
            }

            .title-page {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                page-break-after: always;
            }

            h1.chapter-heading {
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                margin-top: 80px;
                margin-bottom: 20px;
                text-transform: uppercase;
            }

            h2.chapter-subtitle {
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 40px;
                color: #333;
            }

            p {
                margin: 0;
                margin-bottom: 14px;
                text-align: justify;
                text-indent: 2em;
                widows: 2;
                orphans: 2;
            }
        </style>
    </head>
    <body>
        <div class="title-page">{{ title }}</div>

        {% for section in sections %}
            <h1 class="chapter-heading">Chapter {{ loop.index }}</h1>
            <h2 class="chapter-subtitle">{{ section.heading }}</h2>
            {% for para in section.body %}
                <p>{{ para }}</p>
            {% endfor %}
        {% endfor %}
    </body>
    </html>
    """)

    # Parse content into sections
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