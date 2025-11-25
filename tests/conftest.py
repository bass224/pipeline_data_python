import pytest
import pandas as pd
from pathlib import Path

@pytest.fixture
def test_data_dir():
    return Path(__file__).parent / "data"

@pytest.fixture
def users_df(test_data_dir):
    return pd.read_json(test_data_dir / "users_test.json")

@pytest.fixture
def sales_df(test_data_dir):
    return pd.read_csv(test_data_dir / "sales_test.csv")
