import pandas as pd

from pheno_utils import PhenoLoader


def average_left_right_features(df: pd.DataFrame) -> pd.DataFrame:
    left_cols = [col for col in df.columns if col.endswith("_left")]
    for left in left_cols:
        base_name = left[:-5]
        right = f"{base_name}_right"
        if right in df.columns:
            df[base_name] = (df[left] + df[right]) / 2

    cols_to_drop = [
        col for col in df.columns if col.endswith("_left") or col.endswith("_right")
    ]
    return df.drop(columns=cols_to_drop)


def main() -> None:
    loader = PhenoLoader("fundus")

    # Export the full raw table from the TRE workspace.
    raw_df = loader[loader.fields]
    raw_df.to_csv("full_fundus.csv", index=False)

    df = pd.read_csv("full_fundus.csv")

    # Replace this list with the exact non-analytic columns excluded in the study.
    drop_cols = [
        "cohort",
        "research_stage",
    ]
    existing_drop_cols = [col for col in drop_cols if col in df.columns]
    if existing_drop_cols:
        df = df.drop(columns=existing_drop_cols)

    df.to_csv("fundus_age.csv", index=False)

    averaged_df = average_left_right_features(df.copy())
    averaged_df.to_csv("fundus_avg.csv", index=False)


if __name__ == "__main__":
    main()
