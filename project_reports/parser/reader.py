"""
USFM Reader using usfm-grammar
"""

import os
from glob import glob
from usfm_grammar import USFMParser
from .document import Document

class USFMReader:
    def __init__(self):
        self.parser = USFMParser

    def read_directory(self, path):
        """
        Recursively read all .sfm and .usfm files under the given path,
        parse them into USFMDocument objects, and return as a list.
        """
        usfm_files = []
        for pattern in ("*.SFM", "*.USFM"):
            usfm_files.extend(glob(path + "/" + pattern, recursive=True))

        documents = []
        for filepath in usfm_files:
            print(f"Reading file: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            content_parser = USFMParser(content)
            biblenlp_format = content_parser.to_biblenlp_format(ignore_errors=True)
            bible_dict = {k: v for k, v in zip(biblenlp_format["vref"], biblenlp_format["text"])}  # type: ignore
            documents.append(Document(filepath, content, bible_dict))

            # if len(documents) >= 1:
            #     print("Stopping after 1 document for testing purposes.")
            #     break
        return documents
