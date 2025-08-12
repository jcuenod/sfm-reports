"""
Report: Identify characters from unexpected scripts (non-Latin letters)
"""
from .base import BaseReport
import wildebeest.wb_analysis as wb_ana

class WildebeestReport(BaseReport):
    @property
    def name(self) -> str:
        return "wildebeest_report"

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
        return wb.analysis
