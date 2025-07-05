import markdown
from pathlib import Path

# Load README
readme_text = Path("README.md").read_text()

# Convert to HTML
html = markdown.markdown(readme_text)

# Wrap in HTML layout
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Jenkins HTML Deployment Guide</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; overflow-x: auto; }}
        code {{ background-color: #eee; padding: 2px 4px; }}
        table, th, td {{ border: 1px solid black; border-collapse: collapse; padding: 5px; }}
        th {{ background-color: #eee; }}
    </style>
</head>
<body>
{html}
</body>
</html>
"""

# Write to index.html (for NGINX)
Path("index.html").write_text(full_html)
print("✅ README converted to index.html")
