
#on va faire un script qui va lancer tout le pipeline de data engineering : ingestion, transformation,

import uuid
import pandas as pd

from data_pipeline.utils.logger import get_logger
from data_pipeline.utils.paths import RAW_DATA, INTERIM_DATA, PROCESSED_DATA

from data_pipeline.ingestion.ingestion import load_csv, load_json, save_interim
from data_pipeline.transformation.transformation import (
    clean_users,
    clean_sales,
    enrich_sales_with_users,
    save_processed
)


def main():

    # ------------------------------------------------------
    # 1. créer un run_id unique (très utile en production)
    # ------------------------------------------------------
    run_id = str(uuid.uuid4()) #Chaque exécution du pipeline a un ID unique.
    #C’est exactement ce que font Airflow, GCP Dataflow ou Databricks pour tracer un run.

    logger = get_logger(
        name="data_pipeline.run",
        component="pipeline",
        run_id=run_id,
        json_format=True
    )

    logger.info("Pipeline started")

    try:
        # --------------------------------------------------
        # 2. INGESTION
        # --------------------------------------------------
        logger.info("Step 1: Ingestion")

        users = load_json(RAW_DATA / "users.json")
        sales = load_csv(RAW_DATA / "sales.csv")

        save_interim(users, "users_interim")
        save_interim(sales, "sales_interim")

        # --------------------------------------------------
        # 3. TRANSFORMATION
        # --------------------------------------------------
        logger.info("Step 2: Transformation")

        users_clean = clean_users(users)
        sales_clean = clean_sales(sales)

        merged = enrich_sales_with_users(users_clean, sales_clean)

        # --------------------------------------------------
        # 4. EXPORT (Processed)
        # --------------------------------------------------
        logger.info("Step 3: Saving processed data")

        save_processed(merged, "sales_enriched")

        logger.info("Pipeline finished successfully")

    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
