from typing import Iterable, Set
from pandas import DataFrame
from medrisk_features.logging import get_logger


class SchemaValidationError(Exception):
    """Raised when input data schema is invalid."""
    pass


class DataSchemaValidator:
    """
    Validate input dataset schema before feature engineering.

    Purpose
    -------
    Detect missing critical columns early and prevent
    silent failures or inconsistent feature generation.
    """

    # Minimal required columns for the full pipeline
    REQUIRED_COLUMNS: Set[str] = {
        "Age",
        "glucose_fasting",
        "bmi",
    }

    def __init__(self, logger=None):
        self.logger = logger or get_logger(self.__class__.__name__)

    def validate_required_columns(self, df: DataFrame) -> None:
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            message = f"Missing required columns: {sorted(missing)}"
            self.logger.error(message)
            raise SchemaValidationError(message)

        self.logger.info("All required columns are present.")

    def validate(self, df: DataFrame) -> None:
        """
        Run all schema validations.

        Parameters
        ----------
        df : DataFrame
            Input dataset.

        Raises
        ------
        SchemaValidationError
            If schema validation fails.
        """
        self.logger.info("Validating input data schema...")
        self.validate_required_columns(df)
        self.logger.info("Schema validation completed successfully.")