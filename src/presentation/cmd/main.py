from src.domain.services.csv_formatter import CsvFormatter
import sys


def input_from_nifi() -> None:
    # input_data: str = sys.stdin.readlines()
    # print(repr(input_data))
    output: list[str] = CsvFormatter(
        input_stream=sys.stdin.readlines(),
    ).process_csv()
    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)


if __name__ == "__main__":
    input_from_nifi()
