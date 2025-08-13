"""
Project Reports Python Library
"""

from .parser.reader import USFMReader
from .reports.base import BaseReport
from .render_report import generate_html_report
import pkgutil
import importlib
from . import reports


def load_reports():
    """
    Discover and instantiate all report classes in the reports package.
    """
    report_objects = []
    for _, module_name, _ in pkgutil.iter_modules(reports.__path__):
        module = importlib.import_module(f"{__name__}.reports.{module_name}")
        for attr in dir(module):
            cls = getattr(module, attr)
            if isinstance(cls, type) and issubclass(cls, BaseReport) and cls is not BaseReport:
                report_objects.append(cls())
    return report_objects


def run_reports(path, html_filename=None):
    """
    Read all USFM files in the given path and run all discovered reports.
    Returns a dict mapping report name to its results.
    """
    reader = USFMReader()
    documents = reader.read_directory(path)
    results = {}
    reports = load_reports()
    for report in reports:
        results[report.name] = report.run(documents)

    if html_filename:
        generate_html_report(reports, html_filename, "USFM Text Analysis Report")

    return results
