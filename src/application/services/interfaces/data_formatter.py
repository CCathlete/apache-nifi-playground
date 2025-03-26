from abc import ABC, abstractmethod
from src.domain.services.interfaces.formatter import DataFormatter


class PrepareDataForWarehouse(ABC):
    @abstractmethod
    def prepare_csv_to_psql(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def data_formatter(self) -> DataFormatter:
        pass

    @data_formatter.setter
    @abstractmethod
    def data_formatter(self, data_formatter: DataFormatter) -> None:
        pass
