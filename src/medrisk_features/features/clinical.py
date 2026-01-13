import numpy as np
from pandas import DataFrame
from medrisk_features.logging import get_logger


class ClinicalFeatureEngineer:
    """
    Create clinical interaction features and lipid/glycemic ratios.

    Purpose
    -------
    Capture quantitative relationships between biomarkers
    that reflect metabolic balance and cardiovascular risk.

    Medical relevance
    ------------------
    Ratios such as HDL/LDL and cholesterol/HDL are strong
    indicators of cardiometabolic risk beyond raw values.
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger(self.__class__.__name__)

    def transform(self, df: DataFrame) -> DataFrame:
        """
        Apply clinical interaction feature engineering.

        Parameters
        ----------
        df : DataFrame
            Input dataset.

        Returns
        -------
        DataFrame
            Dataset enriched with clinical interaction features.
        """
        df = df.copy()
        self.logger.info("Creating clinical interaction features...")

        # --------------------------------------------------
        # Lipid ratios
        # --------------------------------------------------
        if {"hdl_cholesterol", "ldl_cholesterol"}.issubset(df.columns):
            df["hdl_to_ldl_ratio"] = (
                df["hdl_cholesterol"]
                / df["ldl_cholesterol"].replace(0, np.nan)
            )
        else:
            self.logger.warning(
                "HDL or LDL cholesterol missing — hdl_to_ldl_ratio not created."
            )

        if {"cholesterol_total", "hdl_cholesterol"}.issubset(df.columns):
            df["cholesterol_ratio"] = (
                df["cholesterol_total"]
                / df["hdl_cholesterol"].replace(0, np.nan)
            )
        else:
            self.logger.warning(
                "Total cholesterol or HDL missing — cholesterol_ratio not created."
            )

        # --------------------------------------------------
        # BMI × glucose interaction
        # --------------------------------------------------
        if {"bmi", "glucose_fasting"}.issubset(df.columns):
            df["bmi_glucose_interaction"] = (
                df["bmi"] * df["glucose_fasting"]
            )
        else:
            self.logger.warning(
                "BMI or fasting glucose missing — bmi_glucose_interaction not created."
            )

        # --------------------------------------------------
        # Glycemic variation
        # --------------------------------------------------
        if {"glucose_postprandial", "glucose_fasting"}.issubset(df.columns):
            df["glucose_diff"] = (
                df["glucose_postprandial"] - df["glucose_fasting"]
            )
        else:
            self.logger.warning(
                "Postprandial or fasting glucose missing — glucose_diff not created."
            )

        self.logger.info("Clinical interaction features created successfully.")
        return df