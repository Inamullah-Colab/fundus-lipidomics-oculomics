# 02. Age and Sex Covariate Adjustment for Fundus Features

This step evaluates how retinal fundus traits vary with age while controlling for sex, then identifies features that remain strong enough for downstream multimodal analysis.

## Purpose

- quantify age-feature relationships after accounting for sex,
- correct for multiple testing using Benjamini-Hochberg FDR,
- visualize age distributions, age-wise percentile bands, and sex-stratified boxplots,
- retain the most informative retinal features for integration with lipidomics.

## Statistical approach

For each fundus feature, the script computes a partial Pearson correlation:

- `x = age`
- `y = fundus feature`
- `covar = sex`

For each test it stores:

- partial correlation coefficient `r`,
- p-value,
- 95% confidence interval,
- FDR-adjusted p-value,
- significance flag.

## Visual outputs

The plotting routine combines:

- a KDE panel for the age distribution,
- a central trend panel with percentile bands across age,
- a vertical KDE for the feature distribution,
- a sex-stratified boxplot.

This figure layout supports the manuscript statement that age and sex should be controlled before fundus-lipid association analysis.

## Output files

- `fundus_age_sex_partial_corr_results_fdr.csv`
- `fundus_age_features_plot.png`
- `fundus_age_features_plot.pdf`

## Related manuscript figure

- `Fig_1_age_sex_fundus.pdf`

## File

- `src/02_age_sex_covariate_adjustment.py`
