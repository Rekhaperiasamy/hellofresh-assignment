import pytest
import os
from hf_bi_python_exercise.src.Csv import Csv


@pytest.fixture
def setup_data():
    recipes = [
        {"name": "Easter Leftover Sandwich", "description": "description..."},
        {"name": "Pasta with Pesto Cream Sauce",
         "description": "description..."}
    ]

    avg_list = [
        ['Hard', 'AverageTotalTime', 115],
        ['Medium', 'AverageTotalTime', 42],
        ['Easy', 'AverageTotalTime', 16]
    ]

    yield {
        'recipes': recipes,
        'avg_list': avg_list
    }

    os.remove(str('avg_output.csv'))
    os.remove(str('recipes_output.csv'))
    print('Tear down')


class TestCsv:
    def test_write_dict_to_csv(self, setup_data):
        file_path = 'recipes_output.csv'
        csv_local = Csv()

        csv_local.write_dict_to_csv(
            setup_data['recipes'], file_path, separator='|')

        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_content = csv_file.read()

        expected_content = 'name|description\r\nEaster Leftover Sandwich|description...\r\nPasta with Pesto Cream Sauce|description...\r\n'

        assert csv_content == expected_content

    def test_write_list_to_csv(self, setup_data):
        file_path = 'avg_output.csv'
        csv_local = Csv()

        csv_local.write_list_to_csv(
            setup_data['avg_list'], file_path, separator='|')

        with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_content = csv_file.read()

        expected_content = 'Hard|AverageTotalTime|115\r\nMedium|AverageTotalTime|42\r\nEasy|AverageTotalTime|16\r\n'

        assert csv_content == expected_content
