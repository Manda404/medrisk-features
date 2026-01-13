from pandas import DataFrame

from medrisk_features.logging import get_logger
from medrisk_features.preprocessing import (
    clean_categorical_variables,
    drop_leakage_columns,
)
from medrisk_features.features import (
    DemographicsFeatureEngineer,
    MedicalFeatureEngineer,
    ClinicalFeatureEngineer,
    MetabolicFeatureEngineer,
    BehavioralFeatureEngineer,
    LifestyleFeatureEngineer,
)


class FeatureEngineeringPipeline:
    """
    Complete feature engineering pipeline for medical,
    metabolic and lifestyle risk modeling.

    Purpose
    -------
    Orchestrate all feature transformations in a
    reproducible, explainable and leakage-safe manner.
    """

    def __init__(
        self,
        age_group_strategy: str = "detailed",
        logger=None,
    ):
        self.logger = logger or get_logger(self.__class__.__name__)

        # Initialize feature blocks
        self.demographics = DemographicsFeatureEngineer(
            age_group_strategy=age_group_strategy,
            logger=self.logger,
        )
        self.medical = MedicalFeatureEngineer(logger=self.logger)
        self.clinical = ClinicalFeatureEngineer(logger=self.logger)
        self.metabolic = MetabolicFeatureEngineer(logger=self.logger)
        self.behavioral = BehavioralFeatureEngineer(logger=self.logger)
        self.lifestyle = LifestyleFeatureEngineer(logger=self.logger)

    def transform(self, df: DataFrame) -> DataFrame:
        """
        Apply the full feature engineering pipeline.

        Parameters
        ----------
        df : DataFrame
            Raw input dataset.

        Returns
        -------
        DataFrame
            Fully enriched dataset.
        """
        self.logger.info("Starting feature engineering pipeline...")
        df_enriched = df.copy(deep=True)

        # --------------------------------------------------
        # Step 0: Prevent data leakage
        # --------------------------------------------------
        df_enriched = drop_leakage_columns(df_enriched, logger=self.logger)

        # --------------------------------------------------
        # Step 1: Clean categorical variables
        # --------------------------------------------------
        df_enriched = clean_categorical_variables(
            df_enriched,
            logger=self.logger,
        )

        # --------------------------------------------------
        # Step 2: Demographics
        # --------------------------------------------------
        df_enriched = self.demographics.transform(df_enriched)

        # --------------------------------------------------
        # Step 3: Medical clinical features
        # --------------------------------------------------
        df_enriched = self.medical.transform(df_enriched)

        # --------------------------------------------------
        # Step 4: Clinical interactions
        # --------------------------------------------------
        df_enriched = self.clinical.transform(df_enriched)

        # --------------------------------------------------
        # Step 5: Advanced metabolism
        # --------------------------------------------------
        df_enriched = self.metabolic.transform(df_enriched)

        # --------------------------------------------------
        # Step 6: Behavioral features
        # --------------------------------------------------
        df_enriched = self.behavioral.transform(df_enriched)

        # --------------------------------------------------
        # Step 7: Lifestyle features
        # --------------------------------------------------
        df_enriched = self.lifestyle.transform(df_enriched)

        self.logger.info(
            f"Pipeline completed successfully — total columns: {df_enriched.shape[1]}"
        )
        return df_enriched