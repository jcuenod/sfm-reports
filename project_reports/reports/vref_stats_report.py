"""
Report: Identify characters from unexpected scripts (non-Latin letters)
"""
from .base import BaseReport

VERSES_PER_BOOK = {
    "GEN": 1533, "EXO": 1213, "LEV": 859, "NUM": 1288, "DEU": 959, "JOS": 658,
    "JDG": 618, "RUT": 85, "1SA": 810, "2SA": 695, "1KI": 816, "2KI": 719,
    "1CH": 942, "2CH": 822, "EZR": 280, "NEH": 406, "EST": 167, "JOB": 1070,
    "PSA": 2461, "PRO": 915, "ECC": 222, "SNG": 117, "ISA": 1292, "JER": 1364,
    "LAM": 154, "EZK": 1273, "DAN": 357, "HOS": 197, "JOL": 73, "AMO": 146,
    "OBA": 21, "JON": 48, "MIC": 105, "NAM": 47, "HAB": 56, "ZEP": 53, "HAG": 38,
    "ZEC": 211, "MAL": 55, "MAT": 1071, "MRK": 678, "LUK": 1151, "JHN": 879,
    "ACT": 1007, "ROM": 433, "1CO": 437, "2CO": 257, "GAL": 149, "EPH": 155,
    "PHP": 104, "COL": 95, "1TH": 89, "2TH": 47, "1TI": 113, "2TI": 83,
    "TIT": 46, "PHM": 25, "HEB": 303, "JAS": 108, "1PE": 105, "2PE": 61,
    "1JN": 105, "2JN": 13, "3JN": 15, "JUD": 25, "REV": 404,
}

OT_BOOKS = ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA",
            "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST", "JOB", "PSA",
            "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS",
            "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG",
            "ZEC", "MAL"]
NT_BOOKS = ["MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH",
            "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB",
            "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]

def _render_stat(label, value):
    """Render a statistical item."""
    return f"""
        <div class="stat-item">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>"""

def round_to_nearest(value, nearest=5):
    """Round a number to the nearest specified value."""
    return round(value / nearest) * nearest

class VrefStatsReport(BaseReport):
    @property
    def name(self) -> str:
        return "vref_stats_report"
    
    def render(self):
        """Render the report HTML."""
        return f"""
        <section><h2>Verse Statistics</h2>
        <div class=\"stats-grid\">
            {_render_stat("Total verses", f"{self.data['total_verses']:,}")}
            {_render_stat("Verses in ranges", f"{self.data['ranges']:,}")}
            {_render_stat("OT completion", f"{self.data['ot_completion']}%")}
            {_render_stat("NT completion", f"{self.data['nt_completion']}%")}
        </div>
        <div class=\"row\"><h3>Book Completion</h3>
            <div class="char-grid" style="display: flex; flex-wrap: wrap; gap: 8px; margin-top:1em;">
            {''.join(f'<div class="char-item" style="border:1px solid #ccc; padding:8px; min-width:80px; text-align:center;"><b>{book}</b><br>{self.data["verses_per_book"][book]}%</div>' for book in VERSES_PER_BOOK)}
        </details>
        </section>
        """

    def run(self, documents):
        """
        Count total verses
        Find verses with ranges
        Get book completion stats
        """
        verses_per_book_complete = { book: 0 for book in VERSES_PER_BOOK }
        ranges = 0
        for doc in documents:
            for ref, text in doc.parsed.items():
                if text is None:
                    continue

                book = ref[0:3]
                if "-" in ref:
                    range_terms = ref.split(":")[1].split("-")
                    if len(range_terms) == 2:
                        start, end = int(range_terms[0]), int(range_terms[1])
                        range_size = end - start + 1
                        if start > end:
                            print(f"Invalid range in {ref}: {start} > {end}")
                            range_size = 1
                        ranges += range_size
                    else:
                        print(f"Invalid range format in {ref}")
                
                verses_per_book_complete[book] += 1
        total_verses = sum(verses_per_book_complete.values())
        percentage_complete_per_book = {
            book: round_to_nearest(verses_per_book_complete[book] / VERSES_PER_BOOK[book] * 100)
            for book in VERSES_PER_BOOK
        }

        testament_completion = {
            "OT": round_to_nearest(sum(verses_per_book_complete[book] for book in OT_BOOKS) / sum(VERSES_PER_BOOK[book] for book in OT_BOOKS) * 100),
            "NT": round_to_nearest(sum(verses_per_book_complete[book] for book in NT_BOOKS) / sum(VERSES_PER_BOOK[book] for book in NT_BOOKS) * 100),
        }

        self.data = {
            "total_verses": total_verses,
            "ranges": ranges,
            "verses_per_book": percentage_complete_per_book,
            "ot_completion": testament_completion["OT"],
            "nt_completion": testament_completion["NT"],
        }
        return self.data