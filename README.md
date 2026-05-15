# Integrated Oculomics and Lipidomics Analysis Code

This repository contains the code fragments and figure assets used for the revised manuscript:

**Integrated Oculomics and Lipidomics Reveal Microvascular-Metabolic Signatures Associated with Cardiovascular Health in a Healthy Cohort**

The analysis is based on secondary Human Phenotype Project (HPP) data accessed through the secure Pheno.AI Trusted Research Environment (TRE). The code here is intended to support reproducibility of the reported exploratory association analyses and figure generation. Because the study is observational and cross-sectional, outputs should be interpreted as covariate-adjusted associations rather than causal effects.

This repository is structured to support a journal `Code availability` statement and to make the computational workflow easier to inspect during peer review.

## Code overview

The full public workflow is organised into three code stages:

1. [`src/01_preprocess_hpp_fundus.py`](src/01_preprocess_hpp_fundus.py)
   Extract HPP fundus data inside the TRE, clean fields, and average left/right eye measures.
2. [`src/02_age_sex_covariate_adjustment.py`](src/02_age_sex_covariate_adjustment.py)
   Quantify age-feature associations while adjusting for sex and generate exploratory retinal plots.
3. [`src/03_fundus_lipid_integration.py`](src/03_fundus_lipid_integration.py)
   Merge fundus and lipidomics features, run age/sex-adjusted partial correlations, and generate the main association figures.

## Repository layout

- `src/01_preprocess_hpp_fundus.py`
  HPP/TRE preprocessing for the fundus dataset, including export and left-right eye averaging.
- `src/02_age_sex_covariate_adjustment.py`
  Partial-correlation screening of fundus features against age while adjusting for sex, plus age-density and sex-stratified plots.
- `src/03_fundus_lipid_integration.py`
  Integration of fundus and lipidomics tables with age/sex-adjusted partial correlations, FDR correction, bubble plots, network graphs, and forest plots.
- `docs/01_hpp_fundus_preprocessing.md`
  Markdown explanation of the preprocessing stage.
- `docs/02_age_sex_covariate_adjustment.md`
  Markdown explanation of the age/sex adjustment stage.
- `docs/03_fundus_lipid_integration.md`
  Markdown explanation of the multimodal integration stage.
- `CODE_AVAILABILITY.md`
  Text that can be adapted for the manuscript's required `Code availability` section.
- `CITATION.cff`
  Citation metadata for the repository.
- `REPRODUCIBILITY.md`
  Practical notes on what can and cannot be reproduced outside the TRE.
- `FIGURE_MANIFEST.md`
  Mapping between figure files and their role in the manuscript.

## Expected inputs

The scripts assume access to HPP-derived tabular exports and do not redistribute participant-level data.

- `full_fundus.csv` or direct TRE access through `pheno_utils`
- `fundus_age.csv`
- `fundus_avg.csv`
- `lipids_age.csv`

## Figures in this folder

- `Fig_1_age_sex_fundus.pdf`
  Age- and sex-aware exploratory figure for selected fundus features.
- `Final_bubble_plot.png`
  Bubble plot of top lipid-fundus associations after FDR correction.
- `Network_graphs.png`
  Network view of significant lipid-fundus relationships.
- `Final_forest_plot.png`
  Ranked association summary with confidence intervals.
- `Final_Artery_average_width.png`
- `Final_artery_vessel_density.png`
- `Final_vein_average_width.png`
- `Final_vessel_density.png`
- `fundus_lipid_association_barplot.pdf`

See `FIGURE_MANIFEST.md` for a manuscript-facing summary of these assets.

## Figure preview

### Main association summary

![Bubble plot of top fundus-lipid associations](Final_bubble_plot.png)

![Forest plot of top ranked associations](Final_forest_plot.png)

![Network graph of significant fundus-lipid relationships](Network_graphs.png)

### Feature-specific panels

![Artery average width](Final_Artery_average_width.png)

![Artery vessel density](Final_artery_vessel_density.png)

![Vein average width](Final_vein_average_width.png)

![Vessel density](Final_vessel_density.png)

## Software dependencies

The scripts use standard Python scientific packages:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `pingouin`
- `networkx`
- `statsmodels`
- `pheno_utils`

Install them with:

```bash
pip install -r requirements.txt
```

## Data access

The Human Phenotype Project data are controlled-access. According to the Pheno.AI knowledgebase, users work inside a Trusted Research Environment and can install packages in Jupyter with commands such as `!pip3 install <package name>`. Researchers seeking data access should apply through the official HPP / Pheno.AI process:

- https://knowledgebase.pheno.ai/platform_tutorial.html
- https://knowledgebase.pheno.ai
- https://humanphenotypeproject.org

## Recommended repository naming

For a dedicated public GitHub repository, a clear name would be one of:

- `fundus-lipidomics-oculomics`
- `hpp-fundus-lipidomics-analysis`
- `oculomics-lipidomics-cvd-signatures`

## Notes for manuscript revision

- The code in this repository supports reproducibility of the reported analyses and figure generation.
- The manuscript should include a `Code availability` heading in the Methods section.
- Claims in the manuscript should remain framed as associations derived from secondary cross-sectional data.
- The unpublished revised manuscript file is intentionally excluded from the public repository.
