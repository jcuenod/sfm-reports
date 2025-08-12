# Project Reports Python Library

A modular Python library for reading and parsing USFM (.sfm/.usfm) files and generating a variety of customizable reports. Designed to be extensible: simply add new report classes to the `project_reports/reports` package.

## Installation

1. Clone this repository:
   ```bash
   git clone <repo-url> project-reports
   cd project-reports
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage (Console Output)

```python
from project_reports import run_reports

# Provide the path to a folder containing USFM files
results = run_reports("/path/to/usfm/files")

# `results` is a dict mapping report names to their output data
for name, output in results.items():
    print(f"Report: {name}")
    print(output)
```

To generate an html report, pass the `html_filename` parameter to `run_reports` and it will be exported.

### Command Line Usage

```bash
# Basic console output
python test.py /path/to/usfm/files

# Generate HTML report
python test_html.py --html report.html /path/to/usfm/files
```

## Available Reports

- **token_report**: Tokenize each verse with the NLLB tokenizer, returns max token count and histogram.
- **wildebeest_report**: Finds alphabetic characters outside the Latin script (unexpected scripts).

## Extending with New Reports

1. Create a new `.py` file in `project_reports/reports/`.
2. Import `BaseReport` and subclass it.
3. Implement the `@property name -> str` and `run(self, documents) -> Any` methods.
4. Your report will be auto-discovered by `run_reports()`.

## License

MIT License
