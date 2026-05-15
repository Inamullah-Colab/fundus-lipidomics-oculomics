import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import pingouin as pg
import seaborn as sns
from statsmodels.stats.multitest import multipletests


def run_partial_corr(df_fundus: pd.DataFrame, df_lipid: pd.DataFrame) -> pd.DataFrame:
    for df in [df_fundus, df_lipid]:
        if "sex" in df.columns and df["sex"].dtype == object:
            df["sex"] = df["sex"].astype("category").cat.codes

    df = pd.merge(df_fundus, df_lipid, on="participant_id", suffixes=("_fundus", "_lipid"))
    df["age"] = df["age_fundus"]
    df["sex"] = df["sex_fundus"]
    df.drop(columns=["age_fundus", "sex_fundus", "age_lipid", "sex_lipid"], inplace=True)

    fundus_features = [c for c in df_fundus.columns if c not in ["participant_id", "age", "sex"]]
    lipid_features = [c for c in df_lipid.columns if c not in ["participant_id", "age", "sex"]]

    results = []
    for fundus_feature in fundus_features:
        for lipid_feature in lipid_features:
            sub = df[["age", "sex", fundus_feature, lipid_feature]].dropna()
            if len(sub) < 20:
                continue

            res = pg.partial_corr(
                data=sub,
                x=fundus_feature,
                y=lipid_feature,
                covar=["age", "sex"],
                method="pearson",
            )
            results.append(
                {
                    "fundus_feature": fundus_feature,
                    "lipid_feature": lipid_feature,
                    "r": res["r"].values[0],
                    "p_value": res["p-val"].values[0],
                    "CI_lower": res["CI95%"].iloc[0][0],
                    "CI_upper": res["CI95%"].iloc[0][1],
                    "n": len(sub),
                }
            )

    results_df = pd.DataFrame(results)
    results_df["p_fdr"] = multipletests(results_df["p_value"], method="fdr_bh")[1]
    results_df["significant_fdr"] = results_df["p_fdr"] < 0.05
    return results_df


def plot_bubble(df: pd.DataFrame, selected_fundus: list[str], output_path: str):
    df_sel = df[df["fundus_feature"].isin(selected_fundus)].copy()
    lipid_max_abs_r = df_sel.groupby("lipid_feature")["r"].apply(lambda x: abs(x).max())
    top30_lipids = list(lipid_max_abs_r.sort_values(ascending=False).head(30).index)
    df_top30 = df_sel[df_sel["lipid_feature"].isin(top30_lipids)].copy()

    y_map = {feature: i for i, feature in enumerate(df_top30["fundus_feature"].unique())}
    df_top30["y"] = df_top30["fundus_feature"].map(y_map)

    palette = sns.color_palette("tab20", len(top30_lipids))
    color_dict = dict(zip(top30_lipids, palette))
    df_top30["color"] = df_top30["lipid_feature"].map(color_dict)

    plt.figure(figsize=(14, 10))
    plt.scatter(
        df_top30["r"],
        df_top30["y"],
        s=df_top30["r"].abs() * 1000,
        c=df_top30["color"],
        alpha=0.9,
        edgecolors="black",
    )

    sig_rows = df_top30[df_top30["significant_fdr"]].copy()
    for _, row in sig_rows.iterrows():
        plt.text(row["r"], row["y"] + 0.20, "*", color="red", fontsize=16, ha="center", va="bottom")

    plt.yticks(list(y_map.values()), list(y_map.keys()))
    plt.axvline(0, color="gray", linestyle="--")
    plt.xlabel("Partial Correlation (r)")
    plt.title("Bubble Plot of Top 30 Lipid Features vs Fundus Features (FDR < 0.05)")

    handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            label=lipid,
            color="w",
            markerfacecolor=color_dict[lipid],
            markersize=9,
        )
        for lipid in top30_lipids
    ]
    plt.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left", title="Lipid Feature")
    plt.tight_layout()
    plt.savefig(output_path.replace(".png", ".pdf"))
    plt.savefig(output_path, dpi=600)
    plt.close()
    return color_dict, top30_lipids


def plot_individual_networks(
    df: pd.DataFrame, selected_fundus: list[str], color_dict: dict, output_prefix: str
) -> None:
    df_net = df[(df["fundus_feature"].isin(selected_fundus)) & df["significant_fdr"]]
    hub_counts = df_net.groupby("fundus_feature")["lipid_feature"].nunique()
    hub_fundus = hub_counts[hub_counts > 5].index.tolist()

    for fundus_feature in hub_fundus:
        sub = df_net[df_net["fundus_feature"] == fundus_feature]
        graph = nx.Graph()

        for _, row in sub.iterrows():
            graph.add_edge(
                fundus_feature,
                row["lipid_feature"],
                weight=abs(row["r"]),
                r=row["r"],
                label="*",
            )

        pos = nx.spring_layout(graph, seed=42)
        node_colors = [
            "gray" if node == fundus_feature else color_dict.get(node, "lightgray")
            for node in graph.nodes()
        ]
        node_sizes = [1200 if node == fundus_feature else 900 for node in graph.nodes()]
        edge_colors = ["blue" if data["r"] > 0 else "red" for _, _, data in graph.edges(data=True)]
        edge_widths = [data["weight"] * 4 for _, _, data in graph.edges(data=True)]

        plt.figure(figsize=(9, 6))
        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_sizes)
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors, width=edge_widths, alpha=0.8)
        nx.draw_networkx_labels(graph, pos, font_size=9)
        labels = {(u, v): data["label"] for u, v, data in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels, font_size=10)

        plt.title(f"{fundus_feature} (FDR < 0.05, >5 lipids)")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(f"{output_prefix}_{fundus_feature}.pdf")
        plt.savefig(f"{output_prefix}_{fundus_feature}.png", dpi=600)
        plt.close()


def plot_forest(df: pd.DataFrame, output_path: str, color_dict: dict | None = None) -> None:
    color_dict = color_dict or {}
    df_sig = df[df["significant_fdr"]].copy()
    df_sig = df_sig[df_sig["fundus_feature"] != "average_width"]
    df_top = df_sig.reindex(df_sig["r"].abs().sort_values(ascending=False).index).head(20).copy()
    df_top.reset_index(drop=True, inplace=True)
    df_top["label"] = df_top["fundus_feature"] + " vs " + df_top["lipid_feature"]
    df_top["r_label"] = (
        "r="
        + df_top["r"].round(2).astype(str)
        + " ["
        + df_top["CI_lower"].round(2).astype(str)
        + ", "
        + df_top["CI_upper"].round(2).astype(str)
        + "]"
    )

    fig, ax = plt.subplots(figsize=(11, 8))
    y_pos = np.arange(len(df_top))
    ax.errorbar(
        df_top["r"],
        y_pos,
        xerr=[df_top["r"] - df_top["CI_lower"], df_top["CI_upper"] - df_top["r"]],
        fmt="o",
        color="black",
        ecolor="blue",
        capsize=4,
        markersize=6,
        markerfacecolor="white",
    )

    for i, row in df_top.iterrows():
        ax.plot(
            row["r"],
            y_pos[i],
            "o",
            markersize=7,
            color=color_dict.get(row["lipid_feature"], "black"),
            markeredgecolor="black",
            zorder=3,
        )
        ax.text(
            row["r"],
            y_pos[i] + 0.35,
            row["r_label"],
            fontsize=8,
            ha="center",
            va="bottom",
            bbox=dict(facecolor="white", edgecolor="gray", boxstyle="round,pad=0.3", alpha=0.8),
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_top["label"])
    ax.axvline(0, linestyle="--", color="gray")
    ax.set_xlabel("Partial Correlation (r)")
    ax.set_title("Top 20 Fundus-Lipid Associations (FDR < 0.05)")
    plt.tight_layout()
    plt.savefig(output_path.replace(".png", ".pdf"))
    plt.savefig(output_path, dpi=600)
    plt.close()


def main() -> None:
    df_fundus = pd.read_csv("fundus_avg.csv")
    df_lipid = pd.read_csv("lipids_age.csv")

    selected_fundus = [
        "vein_fractal_dimension",
        "vein_vessel_density",
        "fractal_dimension",
        "vein_average_width",
        "artery_fractal_dimension",
        "vessel_density",
        "artery_vessel_density",
        "artery_distance_tortuosity",
        "artery_tortuosity_density",
        "artery_average_width",
    ]

    results_df = run_partial_corr(df_fundus, df_lipid)
    results_df.to_csv("fundus_lipid_partial_correlations_fdr.csv", index=False)

    color_dict, _ = plot_bubble(results_df, selected_fundus, "bubble_plot_top30.png")
    plot_individual_networks(results_df, selected_fundus, color_dict, "network_graph")
    plot_forest(results_df, "forest_plot_top20.png", color_dict=color_dict)


if __name__ == "__main__":
    main()
