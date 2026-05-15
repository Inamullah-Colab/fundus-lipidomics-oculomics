# Reproducibility Notes

This repository is designed to make the study workflow inspectable, but full reproduction depends on controlled-access Human Phenotype Project data and the Pheno.AI Trusted Research Environment.

## What is reproducible from this repository

- the analysis logic used for preprocessing,
- the partial-correlation workflow,
- the multiple-testing correction strategy,
- the plotting logic for the main visual summaries,
- the code structure needed for journal `Code availability` requirements.

## What is not directly reproducible from this repository alone

- download of participant-level HPP data,
- exact recreation of intermediate CSV files without approved TRE access,
- rerunning the full pipeline outside the HPP governance environment.

## Practical expectation for reviewers and readers

Readers should be able to inspect:

- how left/right fundus variables were averaged,
- how age and sex were incorporated as covariates,
- how fundus and lipidomics tables were merged,
- how statistical significance was adjusted with BH-FDR,
- how the main manuscript figures were produced.

## Recommended manuscript framing

Given the secondary and cross-sectional nature of the data, this repository should be presented as a transparent implementation archive for association analyses rather than a claim of unrestricted end-to-end reproducibility.
