def render_histogram(histogram_data):
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