import pandas as pd
from data_pipeline.transformation.transformation import (
    clean_users, clean_sales, enrich_sales_with_users, save_processed
)

def main():
    users = pd.read_csv("data/interim/users_interim.csv")
    sales = pd.read_csv("data/interim/sales_interim.csv")

    users_clean = clean_users(users)
    sales_clean = clean_sales(sales)

    merged = enrich_sales_with_users(users_clean, sales_clean)

    save_processed(merged, "sales_enriched")

if __name__ == "__main__":
    main()
