"""
Report: Identify characters from unexpected scripts (non-Latin letters)
"""
from .base import BaseReport
import wildebeest.wb_analysis as wb_ana

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

class WildebeestReport(BaseReport):
    @property
    def name(self) -> str:
        return "wildebeest_report"
    
    def render(self):
        
        """Render the wildebeest report section."""
        if not self.data:
            return ""
        
        html = "<section><h2>Character Analysis</h2>"
        
        # Summary stats
        html += _render_summary_stats(self.data)
        
        # Character blocks
        if 'block' in self.data:
            html += _render_character_blocks(self.data['block'])
        
        html += "</section>"
        return html

    def run(self, documents):
        """
        Find all alphabetic characters not in the Latin script.
        Returns a counter of those characters and their counts.
        """
        content = ""
        for doc in documents:
            for _, text in doc.parsed.items():
                content += text + "\n"

        wb = wb_ana.process(string=content)
        self.data = wb.analysis
        return self.data
