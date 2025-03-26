from abc import ABC, abstractmethod


class DataFormatter(ABC):
    """
    A DataFormatter is a class that processes data from stdin, replacing empty values and cleaning up lines.

    Methods:
        process_csv(self) -> list[str]
    """

    @abstractmethod
    def process_csv(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def input_data(self) -> list[str]:
        """
        Getter method.
        Enforcing the input_data property.
        """
        pass

    @input_data.setter
    @abstractmethod
    def input_data(
        self,
        input_data: list[str],
    ) -> None:
        """
        Setter method.
        """
        pass
