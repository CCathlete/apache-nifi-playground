from abc import ABC, abstractmethod


class DataFormatter(ABC):
    """
    A DataFormatter is a class that processes data from stdin, replacing empty values and cleaning up lines.

    Methods:
        process_csv(self) -> list[str]
    """

    @abstractmethod
    def join_categories_to_string(
        self,
        input_data: list[str],
    ) -> list[str]:
        pass

    @abstractmethod
    def convert_to_json(self, data: list[str]) -> list[str]:
        """
        Turns each line in the data into a JSON object.
        """
        pass
