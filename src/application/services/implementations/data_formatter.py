from src.application.services.interfaces.data_formatter import PrepareDataForWarehouse
from src.domain.services.interfaces.formatter import DataFormatter


class SurchargePrepare(PrepareDataForWarehouse):
    """
    An application service for preparing input data for data warehouse.

    Methods:
        prepare_csv_to_psql(self) -> list[str]:

    Properties:
        data_formatter: DataFormatter = a domain service that already contains the input data stream.
    """

    def __init__(self, data_formatter: DataFormatter):
        self.data_formatter = data_formatter

    def prepare_csv_to_psql(self) -> list[str]:
        return self.data_formatter.process_csv()

    # Getters and Setters for enforced properties.
    @property
    def data_formatter(self) -> DataFormatter:
        return self.data_formatter

    @data_formatter.setter
    def data_formatter(self, data_formatter: DataFormatter):
        self.data_formatter = data_formatter
