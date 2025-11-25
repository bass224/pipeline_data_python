from data_pipeline.transformation.transformation import (
    clean_users,
    clean_sales,
    enrich_sales_with_users,
)

def test_clean_users(users_df):
    cleaned = clean_users(users_df)
    assert "user_id" in cleaned.columns
    assert cleaned["user_id"].dtype.kind in "iu"  # int

def test_clean_sales(sales_df):
    cleaned = clean_sales(sales_df)
    assert cleaned["amount"].dtype.kind in "f"   # float

def test_enrichment(users_df, sales_df):
    users_clean = clean_users(users_df)
    sales_clean = clean_sales(sales_df)

    merged = enrich_sales_with_users(users_clean, sales_clean)

    assert len(merged) == 2
    assert "name" in merged.columns
    assert merged["amount"].sum() == 140.5


#Ce test valide le join business.