"""
Report: Generate a beautiful HTML report from all report data
"""
import os
from datetime import datetime


def generate_html_report(reports, output_path="report.html", title="USFM Analysis Report"):
    """
    Generate a beautiful HTML report from the reports list.
    
    Args:
        reports: List of report objects
        output_path: Path where to save the HTML file
        title: Title for the HTML report
    
    Returns:
        str: Path to the generated HTML file
    """
    html_content = _create_html_content(reports, title)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return os.path.abspath(output_path)


def _create_html_content(reports, title):
    """
    Create the HTML content for the report.

    Args:
        reports: List of report objects
        title: Title for the HTML report

    Returns:
        str: HTML content as a string
    """

    reports = [report.render() for report in reports]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {_get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <main>
            {'\n'.join(reports)}
        </main>
    </div>
</body>
</html>"""
    
    return html


def _get_css_styles():
    """Generate CSS styles for the report."""
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""
