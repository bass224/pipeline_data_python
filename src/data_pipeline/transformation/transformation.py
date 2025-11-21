#ici on va créer un module qui va faire la transformation des données : 

"""
Module de transformation des données users et sales.
But :
1) Nettoyer et typer les données users
2) Nettoyer et typer les données sales
3) Enrichir (merge, total par user, features)
4) Sauvegarder en processed/ (CSV + Parquet)

Commentaires en français et petites protections (colonnes manquantes, types invalides).
Dépendances : pandas, numpy, pathlib. Pour Parquet : pyarrow ou fastparquet.
"""


import pandas as pd

from data_pipeline.utils.logger import get_logger
from data_pipeline.utils.paths import INTERIM_DATA, PROCESSED_DATA


logger = get_logger(
    name="data_pipeline.transformation",
    component="transformation",
    json_format=True
)


# --------------------------------------------------------
# 1. CLEANING & NORMALIZATION
# --------------------------------------------------------

def clean_users(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyage et standardisation des données users."""
    
    logger.info("Cleaning users dataframe")

    df = df.copy()

    # normalisation colonnes
    df.columns = [c.lower().strip() for c in df.columns]

    # typage
    df["id"] = df["id"].astype(int)
    df["age"] = df["age"].astype(float)

    # règles de nettoyage
    df = df[df["age"] > 0]           # pas d’âge négatif
    df = df[df["name"].notna()]     # pas de user sans nom

    logger.info(f"Users cleaned: {len(df)} rows")
    return df


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyage et standardisation des données sales."""
    
    logger.info("Cleaning sales dataframe")

    df = df.copy()

    # normalisation colonnes
    df.columns = [c.lower().strip() for c in df.columns]

    # typage
    df["order_id"] = df["order_id"].astype(int)
    df["user_id"] = df["user_id"].astype(int)
    df["amount"] = df["amount"].astype(float)

    # règles business
    df = df[df["amount"] > 0]     # pas de ventes négatives

    logger.info(f"Sales cleaned: {len(df)} rows")
    return df


# --------------------------------------------------------
# 2. ENRICHISSEMENT / JOINS / FEATURES
# --------------------------------------------------------

def enrich_sales_with_users(users_df: pd.DataFrame, sales_df: pd.DataFrame) -> pd.DataFrame:
    """Jointure user ↔ sales + features dérivées."""

    logger.info("Merging users and sales")

    df = sales_df.merge(users_df, left_on="user_id", right_on="id", how="left")

    # Feature engineering
    df["amount_after_tax"] = df["amount"] * 1.20          # TVA 20%
    df["is_big_purchase"] = df["amount"] > 50
    df["age_group"] = pd.cut(df["age"], bins=[0, 25, 40, 60, 100],
                             labels=["Young", "Adult", "Mature", "Senior"])

    logger.info(f"Merged dataframe: {len(df)} rows")
    return df


# --------------------------------------------------------
# 3. SAVE PROCESSED DATA
# --------------------------------------------------------

def save_processed(df: pd.DataFrame, filename: str) -> None:
    """Sauvegarde en CSV et Parquet."""
    
    PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

    csv_path = PROCESSED_DATA / f"{filename}.csv"
    parquet_path = PROCESSED_DATA / f"{filename}.parquet"

    logger.info(f"Saving processed dataset to {csv_path} and {parquet_path}")

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    logger.info("Processed data saved successfully")
