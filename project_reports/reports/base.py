"""
Base class for all reports
"""
from abc import ABC, abstractmethod
from typing import Any, List

class BaseReport(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the report"""
        raise NotImplementedError

    @abstractmethod
    def run(self, documents: List[Any]) -> Any:
        """Run the report against a list of USFMDocument objects"""
        raise NotImplementedError
