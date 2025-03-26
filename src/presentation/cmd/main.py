from src.domain.services.csv_formatter import CsvFormatter
import sys


if __name__ == "__main__":
    # input_data: str = sys.stdin.readlines()
    # print(repr(input_data))
    output = CsvFormatter(
        input_stream=sys.stdin.readlines(),
    ).process_csv()
    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)
