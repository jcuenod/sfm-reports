"""
Report: Token lengths per verse using NLLB tokenizer
"""
from collections import Counter
from transformers import AutoTokenizer

from project_reports.render.histogram import render_histogram
from .base import BaseReport

class TokenReport(BaseReport):
    def __init__(self):
        # Using NLLB distilled model for tokenizing
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    @property
    def name(self):
        return "token_report"

    def render(self):
        """Render the token report section."""
        if not self.data:
            return ""
        
        html = "<section><h2>Token Analysis</h2>"
        
        # Basic stats
        if 'max_tokens' in self.data:
            html += f"""
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{self.data['max_tokens']}</div>
                    <div class="stat-label">Maximum Tokens</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{self.data.get('unk_tokens', 0)}</div>
                    <div class="stat-label">Unknown Tokens</div>
                </div>
            </div>
            """
        
        # Histogram
        if 'histogram' in self.data:
            html += render_histogram(self.data['histogram'])
        
        html += "</section>"
        return html

    def run(self, documents):
        token_counts = []
        unk_tokens = 0
        for doc in documents:
            for ref, text in doc.parsed.items():
                tokens = self.tokenizer.tokenize(text)
                token_counts.append(len(tokens))
                unk_tokens += tokens.count(self.tokenizer.unk_token)
        if not token_counts:
            return {"max_tokens": 0, "histogram": {}}
        max_tokens = max(token_counts)
        histogram = Counter(token_counts)
        self.data = {
            "max_tokens": max_tokens,
            "unk_tokens": unk_tokens,
            "histogram": dict(histogram)
        }
        return self.data
