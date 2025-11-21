
import json
import pandas as pd
from pathlib import Path

from data_pipeline.utils.logger import get_logger
from data_pipeline.utils.paths import RAW_DATA, INTERIM_DATA


logger = get_logger(
    name="data_pipeline.ingestion",
    component="ingestion",
    json_format=True
)


def load_json(file_path: Path) -> pd.DataFrame:
    """
    Charge un fichier JSON en DataFrame.
    """
    logger.info(f"Loading JSON file: {file_path}")

    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    logger.info(f"JSON loaded successfully: {len(df)} rows")
    return df


def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Charge un CSV en DataFrame.
    """
    logger.info(f"Loading CSV file: {file_path}")

    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(file_path)

    df = pd.read_csv(file_path)
    logger.info(f"CSV loaded successfully: {len(df)} rows")
    return df


def save_interim(df: pd.DataFrame, filename: str) -> Path:
    """
    Sauvegarde un DataFrame dans le dossier interim/ en CSV.
    """
    output_path = INTERIM_DATA / filename

    logger.info(f"Saving interim file: {output_path}")
    df.to_csv(output_path, index=False)

    logger.info(f"Interim file saved: {output_path}")
    return output_path
