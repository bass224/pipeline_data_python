
import pandas as pd
from data_pipeline.ingestion.ingestion import load_json, load_csv

def test_load_json(test_data_dir):
    df = load_json(test_data_dir / "users_test.json")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "user_id" in df.columns

def test_load_csv(test_data_dir):
    df = load_csv(test_data_dir / "sales_test.csv")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "amount" in df.columns

"""Ces tests valident :

chargement correct

format DataFrame

colonnes obligatoires

"""