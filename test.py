from project_reports import run_reports
import sys
import pprint
import argparse

from project_reports.render_report import generate_html_report

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate reports from USFM files")
parser.add_argument("path", help="Path to folder containing USFM files")
parser.add_argument("--html", metavar="FILENAME", help="Generate HTML report and save to specified filename")

args = parser.parse_args()

path = args.path
results = run_reports(path, html_filename=args.html)

pprint.pprint(results)

