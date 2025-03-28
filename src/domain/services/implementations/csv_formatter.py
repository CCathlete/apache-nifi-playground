from src.domain.services.interfaces.formatter import DataFormatter
from datetime import datetime, timezone
import regex as re
import json

JsonType = DataFormatter.JsonType


class CsvFormatter(DataFormatter):
    """
    A service that processes input data in csv format.
    """

    def join_categories_to_string(self, input_data):
        return self.join_columns_to_string(input_data)

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

    def convert_to_json(
        self,
        data: list[str],
        json_type: JsonType,
    ) -> list[str]:
        """
        Turns each line in the data into a JSON object after adding id(int) and
        created_at(timestamp).
        NOTE: This logic is not working, timestamp and removal ov invisible characters needed.
        """
        if json_type == JsonType.COMBINED_COLUMNS:
            valid_lines: list[str] = []
            for line in data:
                json_record: dict[str, str | int] = {
                    "id": 1,
                    "content": line,
                    "created_at": int(datetime.now(timezone.utc).timestamp() * 1000),
                }
                valid_lines.append(
                    json.dumps(json_record),
                )
            return valid_lines

        if json_type == JsonType.MAP_CSV_COLUMNS:
            # Loading column mapping from a file
            # Assuming it's located in presentation/cmd.
            with open("column_mapping.json", "r", encoding="utf-8") as f:
                column_mapping: dict[str, str | int] = json.load(f)

            valid_data: bool = (
                data is not None
                and data != [""]
                and data != ["\n"]
                and data != []
                and data != ["\ufeff"]
            )

            json_records: list[str] = []
            if valid_data:
                # Extract column headers (first row)
                csv_headers: list[str] = data[0].strip().split(",")
                data = data[1:]  # Remove the header row

                for line in data:
                    # Removing Byte Order Mark (BOM) and invisible characters
                    # while keeping European letters
                    line = re.sub(r"[^\x20-\x7E\u00A0-\u024F]", "", line).replace(
                        "\ufeff", ""
                    )

                    if not line.strip():  # Skipping empty lines.
                        continue

                    values: list[str] = line.split(
                        ","
                    )  # Splitting the row into values.

                    # Creating a dictionary with column names as keys (using
                    # dictionary comprehension)
                    record: dict[str | int, str] = {
                        # Returning the mapped name is exists or the original
                        # csv column name if not.
                        column_mapping.get(col, col): value
                        for col, value in zip(csv_headers, values)
                    }

                    # Converting the record to a json string and appending it to
                    # the final list.
                    json_records.append(json.dumps(record, ensure_ascii=False))

            return json_records
