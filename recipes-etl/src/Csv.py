import csv


class Csv:
    def write_dict_to_csv(self, data, file_path, separator='|'):
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=data[0].keys(), delimiter=separator)

            csv_writer.writeheader()

            for row in data:
                cleaned_row = {key: value.replace(
                    '\n', ' ') for key, value in row.items()}
                csv_writer.writerow(cleaned_row)

    def write_list_to_csv(self, data, file_path, separator='|'):
        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=separator)
            csv_writer.writerows(data)
