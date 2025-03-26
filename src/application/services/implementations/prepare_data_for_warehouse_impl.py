from src.application.services.interfaces.prepare_data_for_warehouse import (
    PrepareDataForWarehouse,
)
from src.domain.services.interfaces.formatter import DataFormatter


class PrepareDataForWarehouseImpl(PrepareDataForWarehouse):
    """
    An application service for preparing input data for data warehouse.

    Methods:
        join_columns_to_one_string(self) -> list[str]:

    Properties:
        data_formatter: DataFormatter = a domain service that already contains the input data stream.
    """

    def __init__(self, data_formatter: DataFormatter):
        # Bypassing the setter for initial assignment.
        self._data_formatter: DataFormatter = data_formatter

    def join_categories_to_one_string(
        self,
        input_data: list[str],
    ) -> list[str]:
        return self.data_formatter.join_categories_to_string(input_data)

    def prepare_for_bulk_insert(
        self,
        data: list[str],
    ) -> list[str]:
        return self.data_formatter.convert_to_json(data)

    # Getters and Setters for enforced properties.
    @property
    def data_formatter(self) -> DataFormatter:
        return self._data_formatter

    @data_formatter.setter
    def data_formatter(self, data_formatter: DataFormatter):
        self._data_formatter = data_formatter
