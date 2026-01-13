import numpy as np
import pandas as pd
from pandas import DataFrame
from medrisk_features.logging import get_logger


class MedicalFeatureEngineer:
    """
    Create clinically interpretable medical features related to
    glucose metabolism, insulin resistance, BMI and blood pressure.

    Guidelines referenced
    ----------------------
    - ADA (glucose, HbA1c)
    - WHO (BMI)
    - NCEP-ATP III (metabolic syndrome)
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Glycemic status
    # ------------------------------------------------------------------
    def _compute_glucose_status(self, df: DataFrame) -> DataFrame:
        df["glucose_status"] = pd.cut(
            df["glucose_fasting"],
            bins=[0, 99, 125, np.inf],
            labels=["Normal", "Pre-Diabetes", "Diabetes"],
        )

        if "hba1c" in df.columns:
            df["hba1c_category"] = pd.cut(
                df["hba1c"],
                bins=[0, 5.7, 6.4, np.inf],
                labels=["Normal", "Pre-Diabetes", "Diabetes"],
            )
        else:
            self.logger.warning("Column 'hba1c' missing — hba1c_category not created.")

        return df

    # ------------------------------------------------------------------
    # Insulin resistance
    # ------------------------------------------------------------------
    def _compute_homa_ir(self, df: DataFrame) -> DataFrame:
        if "insulin_level" not in df.columns:
            self.logger.warning(
                "Column 'insulin_level' missing — HOMA-IR not computed."
            )
            return df

        df["HOMA_IR"] = (df["glucose_fasting"] * df["insulin_level"]) / 405
        df["insulin_resistance_flag"] = (df["HOMA_IR"] > 2.5).astype(int)
        return df

    # ------------------------------------------------------------------
    # BMI and blood pressure
    # ------------------------------------------------------------------
    def _compute_bmi_and_bp(self, df: DataFrame) -> DataFrame:
        df["bmi_category"] = pd.cut(
            df["bmi"],
            bins=[0, 18.5, 24.9, 29.9, np.inf],
            labels=["Underweight", "Normal", "Overweight", "Obese"],
        )

        if {"systolic_bp", "diastolic_bp"}.issubset(df.columns):

            def bp_category(row):
                if row["systolic_bp"] < 120 and row["diastolic_bp"] < 80:
                    return "Normal"
                elif (120 <= row["systolic_bp"] <= 139) or (
                    80 <= row["diastolic_bp"] <= 89
                ):
                    return "Pre-Hypertension"
                else:
                    return "Hypertension"

            df["bp_category"] = df.apply(bp_category, axis=1)
        else:
            self.logger.warning(
                "Blood pressure columns missing — bp_category not created."
            )

        return df

    # ------------------------------------------------------------------
    # Metabolic syndrome
    # ------------------------------------------------------------------
    def _compute_metabolic_syndrome(self, df: DataFrame) -> DataFrame:
        required = {
            "bmi",
            "systolic_bp",
            "triglycerides",
            "hdl_cholesterol",
            "glucose_fasting",
        }

        if not required.issubset(df.columns):
            self.logger.warning(
                "Missing columns for metabolic syndrome — flag not created."
            )
            return df

        df["metabolic_syndrome_flag"] = (
            (
                (df["bmi"] >= 30).astype(int)
                + (df["systolic_bp"] >= 130).astype(int)
                + (df["triglycerides"] >= 150).astype(int)
                + (df["hdl_cholesterol"] < 40).astype(int)
                + (df["glucose_fasting"] >= 110).astype(int)
            )
            >= 3
        ).astype(int)

        return df

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def transform(self, df: DataFrame) -> DataFrame:
        """
        Apply medical feature engineering.

        Parameters
        ----------
        df : DataFrame
            Input dataset.

        Returns
        -------
        DataFrame
            Dataset enriched with medical features.
        """
        df = df.copy()
        self.logger.info("Creating medical features...")

        if "glucose_fasting" not in df.columns:
            raise KeyError(
                "Column 'glucose_fasting' is required for medical features."
            )

        for step in [
            self._compute_glucose_status,
            self._compute_homa_ir,
            self._compute_bmi_and_bp,
            self._compute_metabolic_syndrome,
        ]:
            df = step(df)

        self.logger.info("Medical features created successfully.")
        return df