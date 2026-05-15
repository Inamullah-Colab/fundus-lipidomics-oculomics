# Code Availability

The custom Python code used for fundus preprocessing, age/sex covariate adjustment, multimodal fundus-lipid integration, and figure generation is available in this repository.

Core analysis scripts:

- `src/01_preprocess_hpp_fundus.py`
- `src/02_age_sex_covariate_adjustment.py`
- `src/03_fundus_lipid_integration.py`

These scripts reproduce the main computational steps reported in the manuscript, including:

- extraction and preprocessing of Human Phenotype Project fundus data within the secure TRE environment,
- adjustment of retinal features for age and sex using partial correlation analysis,
- integration of fundus and lipidomics features with multiple-testing correction, and
- generation of the principal visual summaries used in the manuscript.

Participant-level Human Phenotype Project data are not publicly redistributed through this repository because access is governed by the HPP / Pheno.AI Trusted Research Environment and related privacy controls. Researchers may request access to the underlying data through the official HPP channels:

- https://knowledgebase.pheno.ai
- https://humanphenotypeproject.org

Suggested manuscript wording:

> Code availability: Custom code used for preprocessing, covariate adjustment, multimodal integration, and figure generation is available in the study GitHub repository. Participant-level Human Phenotype Project data are controlled-access and can be requested through the official HPP / Pheno.AI Trusted Research Environment.
