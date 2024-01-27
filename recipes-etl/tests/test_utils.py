import pytest
from src.Utils import Utils


@pytest.fixture
def setup_data():
    data = 5  # Set up a sample number
    print("\nSetting up resources...")
    yield data  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    print("\nTearing down resources...")


class TestUtils:
    def test_extract_time_in_minutes(self, setup_data):
        assert Utils.extract_time_in_minutes("10M") == 10
        assert Utils.extract_time_in_minutes("10H") == 10 * 60
        assert Utils.extract_time_in_minutes("PT5M") == 5
        assert Utils.extract_time_in_minutes("PT8H") == 8 * 60
        assert Utils.extract_time_in_minutes("Random5M") == 5
        assert Utils.extract_time_in_minutes("Random8H") == 8 * 60

        assert Utils.extract_time_in_minutes("10H5M") == 10 * 60 + 5
        assert Utils.extract_time_in_minutes("PT8H10M") == 8 * 60 + 10
        assert Utils.extract_time_in_minutes("Random8H12M") == 8 * 60 + 12

        assert Utils.extract_time_in_minutes(
            "10H5M10H5M") == (10 * 60) + 5 + (10*60) + 5
        assert Utils.extract_time_in_minutes(
            "PT8H10M5M5M") == 8 * 60 + 10 + 5 + 5
        assert Utils.extract_time_in_minutes(
            "Random8H12M3H4H") == (8 * 60) + 12 + (3*60) + (4*60)

        assert Utils.extract_time_in_minutes("PT") == 0
        assert Utils.extract_time_in_minutes("random") == 0
