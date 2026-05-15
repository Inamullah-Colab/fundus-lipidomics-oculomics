# Integrated Oculomics and Lipidomics Analysis Code

Official analysis repository for the revised manuscript:

**Integrated Oculomics and Lipidomics Reveal Microvascular-Metabolic Signatures Associated with Cardiovascular Health in a Healthy Cohort**

This repository contains the public code and figure assets used to support the manuscript's computational workflow. The analysis is based on secondary Human Phenotype Project (HPP) data accessed through the secure Pheno.AI Trusted Research Environment (TRE). Because the study is observational and cross-sectional, outputs should be interpreted as age/sex-adjusted associations rather than causal effects.

This repository is structured to make the analysis workflow easy to inspect during peer review.

---

## Overview

The repository provides:

- preprocessing code for HPP fundus data,
- age- and sex-adjusted retinal feature analysis,
- fundus-lipidomics integration code,
- figure-generation scripts and public figure assets,
- manuscript-facing documentation for code availability and reproducibility.

---

## Key Capabilities

### 1. Fundus preprocessing

Participant-level retinal measurements are prepared from HPP exports, including left/right eye harmonization and creation of averaged fundus features.

### 2. Covariate-adjusted retinal analysis

Fundus traits are tested against age while adjusting for sex using partial Pearson correlation, followed by FDR correction and visual summary panels.
### 3. Fundus-lipid integration

Fundus and lipidomics features are merged on participant identifier, tested using age/sex-adjusted partial correlations, and summarized with bubble plots, network graphs, and forest plots.
### 4. Manuscript-oriented outputs

The repository includes figure assets and text files that can be directly referenced when preparing or revising the manuscript.

---

## Repository Structure

The codebase is organized into modular components reflecting the workflow described in the manuscript:

```text
fundus-lipidomics-oculomics/
|-- src/
|   |-- 01_preprocess_hpp_fundus.py
|   |-- 02_age_sex_covariate_adjustment.py
|   `-- 03_fundus_lipid_integration.py
|-- docs/
|   |-- 01_hpp_fundus_preprocessing.md
|   |-- 02_age_sex_covariate_adjustment.md
|   `-- 03_fundus_lipid_integration.md
|-- examples/
|   `-- README.md
|-- preview_images/
|   |-- Fig_1_age_sex_fundus.png
|   `-- fundus_lipid_association_barplot.png
|-- CODE_AVAILABILITY.md
|-- REPRODUCIBILITY.md
|-- FIGURE_MANIFEST.md
|-- CITATION.cff
|-- requirements.txt
`-- README.md
```

Main analysis scripts:

- [`src/01_preprocess_hpp_fundus.py`](src/01_preprocess_hpp_fundus.py)
- [`src/02_age_sex_covariate_adjustment.py`](src/02_age_sex_covariate_adjustment.py)
- [`src/03_fundus_lipid_integration.py`](src/03_fundus_lipid_integration.py)
- [`examples/README.md`](examples/README.md)

---

## System Requirements

This codebase was prepared for Python-based scientific analysis and uses:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `pingouin`
- `networkx`
- `statsmodels`
- `pheno_utils`

The workflow assumes access to HPP-derived tabular data inside the Pheno.AI TRE or to permitted exported derived files.

Expected input files:

- `full_fundus.csv` or direct TRE access through `pheno_utils`
- `fundus_age.csv`
- `fundus_avg.csv`
- `lipids_age.csv`

---

## Installation

We recommend using a dedicated Python environment.

### 1. Clone the repository

```bash
git clone https://github.com/Inamullah-Colab/fundus-lipidomics-oculomics.git
cd fundus-lipidomics-oculomics
```

### 2. Create and activate an environment

Using Conda:

```bash
conda create -n fundus_lipidomics python=3.10
conda activate fundus_lipidomics
```

Using `venv`:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

The workflow consists of three main stages.

### Step 1. Preprocess HPP fundus data

This script loads fundus data inside the TRE, removes non-analytic columns, averages left/right eye measures, and writes participant-level fundus outputs.

```bash
python src/01_preprocess_hpp_fundus.py
```

Primary outputs:

- `fundus_age.csv`
- `fundus_avg.csv`

### Step 2. Adjust retinal features for age and sex

This script computes partial correlations between age and retinal features while adjusting for sex, applies Benjamini-Hochberg FDR correction, and generates exploratory figure panels.

```bash
python src/02_age_sex_covariate_adjustment.py
```

Primary outputs:

- `fundus_age_sex_partial_corr_results_fdr.csv`
- `fundus_age_features_plot.png`
- `fundus_age_features_plot.pdf`

### Step 3. Integrate fundus and lipidomics features

This script merges the retinal and lipidomics tables, runs age/sex-adjusted partial correlations for all feature pairs, and generates the main manuscript-style summary figures.

```bash
python src/03_fundus_lipid_integration.py
```

Primary outputs:

- `fundus_lipid_partial_correlations_fdr.csv`
- bubble plot PNG/PDF
- network graph PNG/PDF
- forest plot PNG/PDF

For a compact reviewer-facing run guide, see [`examples/README.md`](examples/README.md).

---

## Figure Preview

The figure layout below follows the sequencing used in the revised manuscript, moving from covariate-adjusted retinal screening to multimodal lipid-retina association summaries.

### Figure 1. Covariate-adjusted retinal screening

[Open PDF](Fig_1_age_sex_fundus.pdf)

![Preview of age- and sex-adjusted fundus overview](preview_images/Fig_1_age_sex_fundus.png)

This figure corresponds to the revised manuscript's initial screening stage, where 18 retinal microvascular traits were evaluated against age with sex included as a covariate. Based on statistical significance, effect-size thresholding, and visual interpretability, six key arterial and venous features were prioritized for downstream multimodal analysis.

### Figure 3. Top 30 lipid-retina associations

![Bubble plot of top fundus-lipid associations](Final_bubble_plot.png)

This bubble plot summarizes partial correlations between 30 lipid species and 10 retinal features after adjusting for age and sex. Bubble size reflects effect magnitude, and the revised manuscript highlights arterial traits, especially artery average width, artery vessel density, and vessel density, as the strongest hubs of lipid sensitivity.

### Figure 4. Count of significant lipid associations per fundus feature

[Open PDF](fundus_lipid_association_barplot.pdf)

![Preview of fundus-lipid association barplot](preview_images/fundus_lipid_association_barplot.png)

This barplot complements the bubble plot by quantifying how many lipid species remained significantly associated with each fundus trait after multiple-testing correction. In the revised manuscript, artery average width emerged as the most lipid-associated retinal feature.

### Figures 5-9. Feature-focused and network views

![Network graph of significant fundus-lipid relationships](Network_graphs.png)

![Artery average width](Final_Artery_average_width.png)

![Artery vessel density](Final_artery_vessel_density.png)

![Vein average width](Final_vein_average_width.png)

![Vessel density](Final_vessel_density.png)

These visualizations expand the main association results into feature-centered views. The revised manuscript uses them to show that the strongest signals cluster around a small set of retinal microvascular traits, with network plots highlighting significant links to lipid species and feature-specific panels making the dominant retinal hubs easier to interpret.

### Figure 10. Ranked summary of top significant associations

![Forest plot of top ranked associations](Final_forest_plot.png)

This forest plot displays the strongest age/sex-adjusted fundus-lipid associations ranked by partial correlation magnitude with 95% confidence intervals. In the revised manuscript, artery-based features dominate the strongest negative associations, particularly with TAG and DAG lipid classes.

See [`FIGURE_MANIFEST.md`](FIGURE_MANIFEST.md) for a file-by-file mapping of repository figures to their analytical role.

---

## Data Access

The Human Phenotype Project data are controlled-access and are not redistributed through this repository. According to the Pheno.AI documentation, researchers work inside a Trusted Research Environment and can install required Python packages within that environment as needed.

Official resources:

- https://knowledgebase.pheno.ai/platform_tutorial.html
- https://knowledgebase.pheno.ai
- https://humanphenotypeproject.org

---

## Reproducibility Scope

This repository makes the analytic workflow inspectable, but complete end-to-end reproduction depends on controlled-access HPP data and TRE permissions. It should therefore be interpreted as a transparent implementation archive for association analyses, not as an unrestricted public data package.

Additional manuscript-facing notes:

- [`CODE_AVAILABILITY.md`](CODE_AVAILABILITY.md)
- [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)

---

## Citation

If you use this repository, please cite the associated manuscript and software record described in [`CITATION.cff`](CITATION.cff).
