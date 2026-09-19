from pathlib import Path

import trafilatura


def extract_article(url):
    html = trafilatura.fetch_url(url)
    if not html:
        raise RuntimeError(f"Could not download {url}")

    metadata = trafilatura.extract_metadata(html)
    body = trafilatura.extract(
        html,
        output_format="html",
        include_links=True,
        include_images=True,
    )

    if not body:
        raise RuntimeError(f"Could not extract article from {url}")

    title = metadata.title if metadata and metadata.title else ""
    return title, body


url = "https://www.sfgate.com/sf-culture/article/melania-film-review-21338044.php"

title, body = extract_article(url)

output = Path("extracted_body.html")
output.write_text(
    f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
<h1>{title}</h1>
{body}
</body>
</html>
""",
    encoding="utf-8",
)

print(f"Extracted article saved to {output}")
