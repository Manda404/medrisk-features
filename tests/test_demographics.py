from medrisk_features.features import DemographicsFeatureEngineer


def test_demographics_features_created(full_df, logger):
    fe = DemographicsFeatureEngineer(logger=logger)
    df_out = fe.transform(full_df)

    assert "age_group" in df_out.columns
    assert "age_squared" in df_out.columns
    assert "socioeconomic_vulnerability_flag" in df_out.columns


def test_missing_age_raises_error(full_df, logger):
    df = full_df.drop(columns=["Age"])
    fe = DemographicsFeatureEngineer(logger=logger)

    try:
        fe.transform(df)
        assert False, "Expected KeyError for missing Age"
    except KeyError:
        assert True