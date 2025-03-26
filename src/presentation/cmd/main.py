from src.domain.services.implementations.csv_formatter import CsvFormatter
from src.application.services.implementations.prepare_data_for_warehouse_impl import (
    PrepareDataForWarehouseImpl,
)
from test.test_csv import DATA
import sys
import argparse


def test_input() -> None:
    input_data: list[str] = sys.stdin.readlines()
    print(repr(input_data))


def test_data_join_columns() -> None:
    input_data: list[str] = DATA.split("\n")
    output: list[str] = PrepareDataForWarehouseImpl(
        CsvFormatter(),
    ).join_categories_to_one_string(input_data)

    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)


def join_columns_to_one_string() -> None:
    input_data: list[str] = sys.stdin.readlines()

    # Calling the application service that processes the input data.
    # When passing in a CSV formatter, the join categories will be
    # join columns.
    output: list[str] = PrepareDataForWarehouseImpl(
        CsvFormatter(),
    ).join_categories_to_one_string(input_data)

    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)


def prepare_for_bulk_insertion() -> None:
    """
    Converts each csv line to a json record with added categories.
    """
    input_data: list[str] = sys.stdin.readlines()

    output: list[str] = PrepareDataForWarehouseImpl(
        CsvFormatter(),
    ).prepare_for_bulk_insert(input_data)

    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom logic for NiFi.")
    parser.add_argument(
        "operation",
        type=str,
        help="""
        Which operation to be performed in the NiFi flow.
        Supported operations: [
          test_input,
          join_columns_to_one_string,
          test_data_to_join_columns,
          prepare_for_bulk_insert,
          ]""",
    )
    args = parser.parse_args()

    if args.operation == "test_input":
        test_input()

    if args.operation == "join_columns_to_one_string":
        join_columns_to_one_string()

    if args.operation == "test_data_to_join_columns":
        test_data_join_columns()

    if args.operation == "prepare_for_bulk_insert":
        prepare_for_bulk_insertion()
