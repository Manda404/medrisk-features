from medrisk_features.features import MedicalFeatureEngineer


def test_medical_features_created(full_df, logger):
    fe = MedicalFeatureEngineer(logger=logger)
    df_out = fe.transform(full_df)

    expected_columns = {
        "glucose_status",
        "hba1c_category",
        "HOMA_IR",
        "insulin_resistance_flag",
        "bmi_category",
        "bp_category",
        "metabolic_syndrome_flag",
    }

    for col in expected_columns:
        assert col in df_out.columns