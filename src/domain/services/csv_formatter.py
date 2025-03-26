import sys


def process_csv(input_stream: list[str]) -> list[str]:
    """Processes CSV data from stdin, replacing empty values and cleaning up lines."""

    valid_lines: list[str] = []

    for line in input_stream:
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
    output = process_csv(sys.stdin.readlines())
    print("\n".join(output), end="")  # Print to stdout (NiFi will capture this)
