"""
Report: Token lengths per verse using NLLB tokenizer
"""
from collections import Counter
from transformers import AutoTokenizer
from .base import BaseReport

class TokenReport(BaseReport):
    def __init__(self):
        # Using NLLB distilled model for tokenizing
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    @property
    def name(self):
        return "token_report"

    def run(self, documents):
        token_counts = []
        for doc in documents:
            for ref, text in doc.parsed.items():
                tokens = self.tokenizer.tokenize(text)
                token_counts.append(len(tokens))
        if not token_counts:
            return {"max_tokens": 0, "histogram": {}}
        max_tokens = max(token_counts)
        histogram = Counter(token_counts)
        return {"max_tokens": max_tokens, "histogram": dict(histogram)}
