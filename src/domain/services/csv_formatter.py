import sys


class CsvFormatter:

    def __init__(
        self,
        input_stream: list[str],
    ) -> None:
        self.input_stream: list[str] = input_stream

    def process_csv(self) -> list[str]:
        """Processes CSV data from stdin, replacing empty values and cleaning up lines."""

        valid_lines: list[str] = []

        for line in self.input_stream:
            line = line.strip().replace(":", "-")  # Remove leading/trailing whitespace

            # Remove trailing underscores
            # line = line.rstrip("_")

            # Remove empty lines
            if not all(value.strip() == "" for value in line.split(",")):
                # Process each value in the line
                processed_values: list[str] = [
                    value.strip() if value.strip() else "_" for value in line.split(",")
                ]
                valid_lines.append(",".join(processed_values).rstrip("_"))

        return valid_lines


# Read from stdin and process the data
if __name__ == "__main__":
    # input_data: str = sys.stdin.readlines()
    # print(repr(input_data))
    output = CsvFormatter(
        input_stream=sys.stdin.readlines(),
    ).process_csv()
    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)
