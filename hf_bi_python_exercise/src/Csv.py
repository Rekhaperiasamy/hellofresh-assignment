import csv


class Csv:
    def write_dict_to_csv(self, data, file_path, separator='|'):
        """
        Write a list of dictionaries to a CSV file.

        Parameters:
        - data (list): A list of dictionaries where each dictionary represents a row of data.
        - file_path (str): The file path where the CSV file will be created or overwritten.
        - separator (str, optional): The delimiter used to separate values in the CSV file.
        Defaults to '|'.

        The method opens the specified CSV file, writes the header using the keys of the first
        dictionary in the data list, and then writes each row of data to the CSV file.
        Any newline characters in the values of the data are replaced with spaces.
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=data[0].keys(), delimiter=separator)

            csv_writer.writeheader()

            for row in data:
                cleaned_row = {key: value.replace(
                    '\n', ' ') for key, value in row.items()}
                csv_writer.writerow(cleaned_row)

    def write_list_to_csv(self, data, file_path, separator='|'):
        """
        Write a list of values to a CSV file.

        Parameters:
        - data (list): A list of values where each value represents a row of data.
        - file_path (str): The file path where the CSV file will be created or overwritten.
        - separator (str, optional): The delimiter used to separate values in the CSV file.
        Defaults to '|'.

        The method opens the specified CSV file, writes each value as a row in the CSV file.
        Any newline characters in the values are replaced with spaces.
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=separator)
            csv_writer.writerows(data)
