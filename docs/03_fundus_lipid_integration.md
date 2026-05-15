# 03. Fundus-Lipid Integration After Age/Sex Adjustment

This step merges the fundus and lipidomics tables and tests pairwise associations while adjusting for age and sex.

## Purpose

- combine fundus-derived retinal features and lipidomic features,
- estimate direct fundus-lipid relationships independent of age and sex,
- apply FDR correction across the full set of pairwise tests,
- generate publication figures for interpretation of the strongest associations.

## Statistical approach

The integration script:

1. merges `fundus_avg.csv` and `lipids_age.csv` on `participant_id`,
2. keeps age and sex as covariates,
3. computes partial Pearson correlations for each fundus-lipid pair,
4. stores `r`, p-value, 95% CI, sample size, and BH-FDR adjusted p-values.

Pairs with fewer than 20 complete observations are skipped.

## Visual outputs

The script generates three main figure types that mirror the manuscript narrative:

- bubble plots for the strongest fundus-lipid associations,
- network graphs to highlight hub-like fundus traits and connected lipid species,
- forest plots summarizing the top ranked significant associations with confidence intervals.

## Expected outputs

- bubble plot PNG/PDF
- network graph PNG/PDF series
- forest plot PNG/PDF

## Related figure assets currently in this folder

- `Final_bubble_plot.png`
- `Network_graphs.png`
- `Final_forest_plot.png`
- `Final_Artery_average_width.png`
- `Final_artery_vessel_density.png`
- `Final_vein_average_width.png`
- `Final_vessel_density.png`
- `fundus_lipid_association_barplot.pdf`

## Interpretation note

These analyses are exploratory and cross-sectional. The resulting figures support statements about age/sex-adjusted associations and shared biological patterns, but they should not be framed as causal evidence.

## File

- `src/03_fundus_lipid_integration.py`
