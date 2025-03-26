from src.domain.services.interfaces.formatter import DataFormatter


class CsvFormatter(DataFormatter):
    """
    A service that processes input data in csv format.
    """

    def join_categories_to_string(self, input_data):
        return self.join_categories_to_string(input_data)

    def join_columns_to_string(
        self,
        input_data: list[str],
    ) -> list[str]:
        """Processes CSV data from stdin, replacing empty values and cleaning up lines."""

        valid_lines: list[str] = []

        for line in input_data:
            line = line.strip().replace(":", "-")  # Remove leading/trailing whitespace

            # Remove empty lines
            if not all(value.strip() == "" for value in line.split(",")):
                # Process each value in the line
                processed_values: list[str] = [
                    value.strip() if value.strip() else "_" for value in line.split(",")
                ]
                valid_lines.append(",".join(processed_values).rstrip("_"))

        return valid_lines
