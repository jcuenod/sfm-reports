"""
Report: Generate a beautiful HTML report from all report data
"""
import json
import os
from datetime import datetime


def generate_html_report(results_dict, output_path="report.html", title="USFM Analysis Report"):
    """
    Generate a beautiful HTML report from the results dictionary.
    
    Args:
        results_dict: Dictionary containing all report results
        output_path: Path where to save the HTML file
        title: Title for the HTML report
    
    Returns:
        str: Path to the generated HTML file
    """
    html_content = _create_html_content(results_dict, title)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return os.path.abspath(output_path)


def _create_html_content(results, title):
    """
    Create the HTML content for the report.

    Args:
        results: Dictionary containing all report results
        title: Title for the HTML report

    Returns:
        str: HTML content as a string
    """
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
            {_render_token_report(results.get('token_report', {}))}
            {_render_wildebeest_report(results.get('wildebeest_report', {}))}
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


def _render_token_report(token_data):
    """Render the token report section."""
    if not token_data:
        return ""
    
    html = "<section><h2>Token Analysis</h2>"
    
    # Basic stats
    if 'max_tokens' in token_data:
        html += f"""
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{token_data['max_tokens']}</div>
                <div class="stat-label">Maximum Tokens</div>
            </div>
        </div>
        """
    
    # Histogram
    if 'histogram' in token_data:
        html += _render_histogram(token_data['histogram'])
    
    html += "</section>"
    return html


def _render_histogram(histogram_data):
    """Render histogram as HTML/CSS bars."""
    if not histogram_data:
        return ""
    
    max_tokens = max(histogram_data.keys())
    max_count = max(histogram_data.values())
    
    html = """<div class="histogram">
        <h3>Token Length Distribution</h3>
        <div class="histogram-container">"""

    # Create bars for each value from 0 to max_tokens
    for i in range(max_tokens + 1):
        count = histogram_data.get(i, 0)
        height = (count / max_count * 280) if max_count > 0 else 0
        
        # Only show labels for every 5th bar or significant points
        label = str(i) if i % 5 == 0 or count > 0 else ""
        
        html += f"""
            <div class="histogram-bar" style="height: {height}px;" title="Length {i}: {count} occurrences">
                {f'<div class="histogram-label">{label}</div>' if label else ''}
            </div>"""
    
    html += "</div></div>"
    return html


def _render_wildebeest_report(wildebeest_data):
    """Render the wildebeest report section."""
    if not wildebeest_data:
        return ""
    
    html = "<section><h2>Character Analysis</h2>"
    
    # Summary stats
    html += _render_summary_stats(wildebeest_data)
    
    # Character blocks
    if 'block' in wildebeest_data:
        html += _render_character_blocks(wildebeest_data['block'])
    
    html += "</section>"
    return html


def _render_summary_stats(data):
    """Render summary statistics."""
    html = "<h3>Summary Statistics</h3><div class=\"stats-grid\">"
    
    stats = [
        ('Total Characters', data.get('n_characters', 0)),
        ('Total Lines', data.get('n_lines', 0)),
    ]
    
    # Add script summaries
    for script_type in ['letter-script', 'number-script']:
        if script_type in data:
            for script, info in data[script_type].items():
                stats.append((f'{script} Characters', info.get('count', 0)))
    
    for label, value in stats:
        html += f"""
        <div class="stat-item">
            <div class="stat-value">{value:,}</div>
            <div class="stat-label">{label}</div>
        </div>"""
    
    html += "</div>"
    return html


def _render_character_blocks(blocks):
    """Render character blocks in organized sections."""
    html = "<h3>Character Details</h3>"
    
    # Group blocks by type
    letter_blocks = {}
    punct_blocks = {}
    other_blocks = {}
    
    for block_name, chars in blocks.items():
        if 'LATIN' in block_name or 'LETTER' in block_name:
            letter_blocks[block_name] = chars
        elif 'PUNCTUATION' in block_name:
            punct_blocks[block_name] = chars
        else:
            other_blocks[block_name] = chars
    
    # Render letter blocks
    if letter_blocks:
        html += "<h4>Letters</h4><div class=\"rows\">"
        for block_name, chars in letter_blocks.items():
            html += f"<div class=\"row\"><h4>{block_name.replace('_', ' ').title()}</h4>"
            html += _render_character_grid(chars)
            html += "</div>"
        html += "</div>"
    
    # Render other blocks
    if other_blocks:
        html += "<h4>Other Characters</h4><div class=\"rows\">"
        for block_name, chars in other_blocks.items():
            html += f"<div class=\"row\"><h4>{block_name.replace('_', ' ').title()}</h4>"
            html += _render_character_grid(chars)
            html += "</div>"
        html += "</div>"
    
    return html


def _render_character_grid(chars):
    """Render a grid of characters."""
    html = "<div class=\"char-grid\">"
    
    # Sort characters by count (descending)
    sorted_chars = sorted(chars.items(), key=lambda x: x[1].get('count', 0), reverse=True)
    
    for char, info in sorted_chars:
        char_display = char if char.isprintable() and char != ' ' else repr(char)
        examples = ", ".join([ex[0][:10] for ex in info.get('ex', [])[:3]])
        
        html += f"""
        <div class="char-item">
            <div class="char-name">'{char_display}' ({info.get('name', 'Unknown')})</div>
            <div class="char-code">{info.get('id', 'Unknown')}</div>
            <div class="char-count">{info.get('count', 0):,} occurrences</div>
            {f'<div class="char-examples">Examples: {examples}</div>' if examples else ''}
        </div>"""
    
    html += "</div>"
    return html