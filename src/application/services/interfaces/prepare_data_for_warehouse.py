from abc import ABC, abstractmethod
from src.domain.services.interfaces.formatter import DataFormatter


class PrepareDataForWarehouse(ABC):
    @abstractmethod
    def join_categories_to_one_string(
        self,
        input_data: list[str],
    ) -> list[str]:
        pass

    @abstractmethod
    def prepare_for_bulk_insert(
        self,
        input_data: list[str],
    ) -> list[str]:
        pass

    @property
    @abstractmethod
    def data_formatter(self) -> DataFormatter:
        pass

    @data_formatter.setter
    @abstractmethod
    def data_formatter(self, data_formatter: DataFormatter) -> None:
        pass
