"""
Base class for all reports
"""
from abc import ABC, abstractmethod
from typing import Any, List
import pprint

class BaseReport(ABC):
    data: Any = {}

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the report"""
        raise NotImplementedError

    def render(self) -> str:
        """Render the report as HTML"""
        if not self.data:
            return f"""
            <section><h2>{self.name.replace('_', ' ').title()}</h2>
            <p>No data available.</p>
            </section>
            """
        return f"""
        <section><h2>{self.name.replace('_', ' ').title()}</h2>
        <pre>{pprint.pformat(self.data)}</pre>
        </section>
        """

    @abstractmethod
    def run(self, documents: List[Any]) -> Any:
        """Run the report against a list of USFMDocument objects"""
        raise NotImplementedError
