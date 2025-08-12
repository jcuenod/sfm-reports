"""
Report: Punctuation usage across USFM files
"""
from collections import Counter
import regex as re
from .base import BaseReport

# Match any Unicode punctuation character
_PUNCT_REGEX = re.compile(r"\p{P}")
# Common quotation mark characters
_QUOTE_CHARS = ['"', '“', '”', '«', '»', '„', '‟', '‹', '›', '‘', '’']

class PunctuationReport(BaseReport):
    @property
    def name(self) -> str:
        return "punctuation_report"

    def run(self, documents):
        punct_counter = Counter()
        quote_counter = Counter()

        for doc in documents:
            # count all punctuation
            for char in _PUNCT_REGEX.findall(doc.raw):
                punct_counter[char] += 1
                if char in _QUOTE_CHARS:
                    quote_counter[char] += 1

        return {
            "punctuation_counts": dict(punct_counter),
            "quote_counts": dict(quote_counter)
        }
