from src.domain.services.implementations.csv_formatter import CsvFormatter
import sys
import argparse


def test_input() -> None:
    input_data: list[str] = sys.stdin.readlines()
    print(repr(input_data))


def join_columns_to_one_string() -> None:
    output: list[str] = CsvFormatter(
        input_stream=sys.stdin.readlines(),
    ).process_csv()
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
          join_columns_to_one_string
          ]""",
    )
    args = parser.parse_args()

    if args.operation == "test_input":
        test_input()

    if args.operation == "join_columns_to_one_string":
        join_columns_to_one_string()
