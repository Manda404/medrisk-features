from pandas import DataFrame
from medrisk_features.logging import get_logger


class LifestyleFeatureEngineer:
    """
    Create lifestyle-related composite features.

    Purpose
    -------
    Summarize global lifestyle quality through
    interpretable and preventive indicators.

    Medical relevance
    ------------------
    Healthy lifestyle improves insulin sensitivity,
    reduces chronic inflammation and lowers diabetes risk.
    """

    def __init__(self, logger=None):
        self.logger = logger or get_logger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Lifestyle score
    # ------------------------------------------------------------------
    def _compute_lifestyle_score(self, df: DataFrame) -> DataFrame:
        required = {
            "diet_score",
            "physical_activity_minutes_per_week",
            "sleep_hours_per_day",
            "alcohol_consumption_per_week",
            "smoking_status",
        }

        if not required.issubset(df.columns):
            self.logger.warning(
                "Missing columns for lifestyle_score — score not created."
            )
            return df

        def lifestyle(row):
            score = 0
            score += 2 if row["diet_score"] >= 6 else 0
            score += 2 if row["physical_activity_minutes_per_week"] >= 150 else 0
            score += 2 if 7 <= row["sleep_hours_per_day"] <= 9 else 0
            score += 2 if row["alcohol_consumption_per_week"] <= 2 else 0
            score += 2 if row["smoking_status"] == "Never" else 0
            return score

        df["lifestyle_score"] = df.apply(lifestyle, axis=1)
        return df

    # ------------------------------------------------------------------
    # Sleep efficiency
    # ------------------------------------------------------------------
    def _compute_sleep_efficiency(self, df: DataFrame) -> DataFrame:
        if {"sleep_hours_per_day", "screen_time_hours_per_day"}.issubset(df.columns):
            df["sleep_efficiency"] = (
                df["sleep_hours_per_day"]
                / (df["screen_time_hours_per_day"] + 1)
            ).clip(upper=2)
        else:
            self.logger.warning(
                "Missing sleep or screen time columns — sleep_efficiency not created."
            )
        return df

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def transform(self, df: DataFrame) -> DataFrame:
        """
        Apply lifestyle feature engineering.

        Parameters
        ----------
        df : DataFrame
            Input dataset.

        Returns
        -------
        DataFrame
            Dataset enriched with lifestyle features.
        """
        df = df.copy()
        self.logger.info("Creating lifestyle features...")

        df = self._compute_lifestyle_score(df)
        df = self._compute_sleep_efficiency(df)

        self.logger.info("Lifestyle features created successfully.")
        return df