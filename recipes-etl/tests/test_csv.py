import pytest
from src.Csv import Csv


@pytest.fixture
def setup_data():
    data = 5  # Set up a sample number
    print("\nSetting up resources...")
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    print("\nTearing down resources...")


class TestCsv:
    def test_filter_recipes(self, setup_data):
        print(setup_data)
        csv = Csv()
