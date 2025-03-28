from abc import ABC, abstractmethod
from enum import Enum


class DataFormatter(ABC):
    """
    A DataFormatter is a class that processes data from stdin, replacing empty values and cleaning up lines.

    Methods:
        process_csv(self) -> list[str]
    """

    class JsonType(Enum):
        COMBINED_COLUMNS = 1
        MAP_CSV_COLUMNS = 2

    @abstractmethod
    def join_categories_to_string(
        self,
        input_data: list[str],
    ) -> list[str]:
        pass

    @abstractmethod
    def convert_to_json(
        self,
        data: list[str],
        json_type: JsonType,
    ) -> list[str]:
        """
        Turns each line in the data into a JSON object.
        """
        pass
