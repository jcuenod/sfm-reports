"""
Document abstraction containing raw and parsed USFM content
"""
from typing import Any

class Document:
    """
    Represents a USFM file with its path, raw content, and parsed object.
    """
    def __init__(self, filepath: str, raw: str, parsed: Any):
        self.filepath = filepath
        self.raw = raw
        self.parsed = parsed
