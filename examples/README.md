# Examples

This folder provides reviewer-friendly examples of how to run the public workflow once the required controlled-access input files are available inside the HPP / Pheno.AI Trusted Research Environment.

## Example 1. Preprocess fundus data

Run:

```bash
python src/01_preprocess_hpp_fundus.py
```

Expected outputs:

- `fundus_age.csv`
- `fundus_avg.csv`

Purpose:

- loads the HPP fundus resource,
- removes non-analytic columns,
- averages left/right eye features to participant level.

## Example 2. Age/sex-adjusted retinal analysis

Run:

```bash
python src/02_age_sex_covariate_adjustment.py
```

Expected outputs:

- `fundus_age_sex_partial_corr_results_fdr.csv`
- `fundus_age_features_plot.png`
- `fundus_age_features_plot.pdf`

Purpose:

- computes partial correlations between age and retinal features,
- adjusts for sex,
- applies BH-FDR correction,
- creates exploratory retinal panels.

## Example 3. Fundus-lipidomics integration

Run:

```bash
python src/03_fundus_lipid_integration.py
```

Expected outputs:

- `fundus_lipid_partial_correlations_fdr.csv`
- `bubble_plot_top30.png`
- `bubble_plot_top30.pdf`
- `forest_plot_top20.png`
- `forest_plot_top20.pdf`
- `network_graph_*.png`
- `network_graph_*.pdf`

Purpose:

- merges participant-level fundus and lipidomics tables,
- computes age/sex-adjusted partial correlations,
- highlights significant associations with figure outputs suitable for manuscript use.

## Notes

- These examples assume the user already has approved access to the HPP / Pheno.AI TRE.
- Participant-level data are not included in this repository.
- Exact output file names may vary slightly if the scripts are adapted for different figure naming conventions.
