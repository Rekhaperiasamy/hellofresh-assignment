import pytest
import csv
import io
from mock import patch, call
from hf_bi_python_exercise.src.Csv import Csv


@pytest.fixture
def setup_data():
    recipes = [
        {"name": "Easter Leftover Sandwich", "description": "description..."},
        {"name": "Pasta with Pesto Cream Sauce",
         "description": "description..."},
        {"name": "Herb Roasted Pork Tenderloin with Preserves",
         "description": "description..."}
    ]
    print("\nSetting up resources...")
    yield {
        "recipes": recipes
    }
    print("Tear down")


class TestCsv:
    def test_write_dict_to_csv(self, setup_data, mocker):
        csv_local = Csv()

        mock_open_func = mocker.mock_open()
        mock_dict_writer = mocker.patch.object(csv, 'DictWriter')

        with patch('builtins.open', mock_open_func):
            csv_local.write_dict_to_csv(
                setup_data["recipes"], 'output.csv', separator='|')

        mock_open_func.assert_called_once_with(
            'output.csv', 'w', newline='', encoding='utf-8')

        mock_dict_writer.assert_called_once_with(
            mock_open_func(), fieldnames=setup_data["recipes"][0].keys(), delimiter='|')

        csv_instance = mock_dict_writer.return_value
        csv_instance.writeheader.assert_called_once()

        expected_calls = [call(setup_data["recipes"][0]),
                          call(setup_data["recipes"][1]),
                          call(setup_data["recipes"][2])]
        csv_instance.writerow.assert_has_calls(expected_calls)
