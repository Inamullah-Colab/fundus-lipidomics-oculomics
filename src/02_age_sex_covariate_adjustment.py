import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pingouin as pg
import seaborn as sns
from statsmodels.stats.multitest import multipletests


def compute_partial_correlations(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    results = []
    for feat in features:
        corr_res = pg.partial_corr(data=df, x="age", y=feat, covar="sex", method="pearson")
        results.append(
            {
                "feature": feat,
                "r": corr_res["r"].values[0],
                "p_value": corr_res["p-val"].values[0],
                "CI_lower": corr_res["CI95%"][0][0],
                "CI_upper": corr_res["CI95%"][0][1],
            }
        )

    results_df = pd.DataFrame(results)
    reject, pvals_corrected, _, _ = multipletests(
        results_df["p_value"], alpha=0.05, method="fdr_bh"
    )
    results_df["p_fdr"] = pvals_corrected
    results_df["significant_fdr"] = reject
    return results_df


def plot_age_sex_panels(
    df: pd.DataFrame, features: list[str], results_df: pd.DataFrame
) -> None:
    fig = plt.figure(figsize=(20, 32))
    outer = fig.add_gridspec(6, 3, wspace=0.25, hspace=0.35)

    for idx, feat in enumerate(features):
        r_val = results_df.loc[results_df["feature"] == feat, "r"].values[0]
        p_val = results_df.loc[results_df["feature"] == feat, "p_value"].values[0]
        ci_lower = results_df.loc[results_df["feature"] == feat, "CI_lower"].values[0]
        ci_upper = results_df.loc[results_df["feature"] == feat, "CI_upper"].values[0]
        sig = results_df.loc[results_df["feature"] == feat, "significant_fdr"].values[0]

        row, col = divmod(idx, 3)
        gs = outer[row, col].subgridspec(
            3, 2, height_ratios=[0.5, 4, 3], width_ratios=[4, 1], hspace=0.3, wspace=0.1
        )
        ax_hist = fig.add_subplot(gs[0, 0])
        ax_main = fig.add_subplot(gs[1, 0])
        ax_kde = fig.add_subplot(gs[1, 1], sharey=ax_main)
        ax_box = fig.add_subplot(gs[2, 0])

        sns.kdeplot(df["age"], bw_adjust=0.5, fill=True, color="blue", ax=ax_hist)
        ax_hist.set_xlim(40, 70)
        ax_hist.axis("off")

        grp = df.groupby(df["age"].astype(int))[feat]
        ages = grp.mean().index.values
        p10, p90 = grp.quantile(0.1).values, grp.quantile(0.9).values
        p20, p80 = grp.quantile(0.2).values, grp.quantile(0.8).values
        p30, p70 = grp.quantile(0.3).values, grp.quantile(0.7).values
        med = grp.median().values

        p20 = np.maximum(p20, p10)
        p80 = np.minimum(p80, p90)
        p30 = np.maximum(p30, p10)
        p70 = np.minimum(p70, p90)

        ax_main.fill_between(ages, p10, p90, color="red", alpha=0.4)
        ax_main.fill_between(ages, p20, p80, color="red", alpha=0.6)
        ax_main.fill_between(ages, p30, p70, color="red", alpha=0.8)
        ax_main.plot(ages, med, color="black", linewidth=2)

        ax_main.set_xlim(40, 70)
        ax_main.set_xticks([40, 50, 60, 70])
        ax_main.set_ylim(p10.min(), p90.max())
        ax_main.set_xlabel("Age (years)")
        ax_main.set_ylabel(feat.replace("_", " ").title())

        star = " *" if sig else ""
        ax_main.text(
            40.1,
            p90.max(),
            f"r = {r_val:.2f} [{ci_lower:.2f}, {ci_upper:.2f}] p={p_val:.3g}{star}",
            va="bottom",
            ha="left",
            fontsize=10,
            fontweight="bold",
            backgroundcolor="white",
        )

        ax_main.spines["top"].set_visible(False)
        ax_main.spines["right"].set_visible(False)

        sns.kdeplot(y=df[feat].dropna(), ax=ax_kde, fill=True, color="lightgray")
        ax_kde.axis("off")

        sns.boxplot(x="sex", y=feat, data=df, palette=["#4C72B0", "#DD8452"], ax=ax_box, width=0.6)
        ax_box.set_xticks([1, 0])
        ax_box.set_xticklabels(["Male", "Female"], fontsize=10)
        ax_box.set_xlabel("Sex")
        ax_box.set_ylabel("")

    plt.tight_layout(pad=0.5)
    fig.savefig("fundus_age_features_plot.png", dpi=300, bbox_inches="tight")
    fig.savefig("fundus_age_features_plot.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    df = pd.read_csv("fundus_avg.csv")

    if df["sex"].dtype == object:
        df["sex"] = df["sex"].astype("category").cat.codes

    exclude_cols = ["age", "sex", "participant_id"]
    all_features = [col for col in df.columns if col not in exclude_cols]
    top_features = all_features[:18]

    results_df = compute_partial_correlations(df, top_features)
    results_df.to_csv("fundus_age_sex_partial_corr_results_fdr.csv", index=False)
    plot_age_sex_panels(df, top_features, results_df)

    sig_features = results_df[results_df["significant_fdr"]].copy()
    sig_features = sig_features[sig_features["r"].abs() >= 0.2]
    print(sig_features[["feature", "r", "p_fdr"]])


if __name__ == "__main__":
    main()
