# 01. HPP Fundus Preprocessing

This step prepares the Human Phenotype Project fundus dataset for downstream analysis inside the Pheno.AI Trusted Research Environment.

## Purpose

- load the fundus study using `pheno_utils`,
- inspect the available fundus and demographic fields,
- export the raw table to CSV for local processing inside the TRE,
- drop non-analytic columns, and
- average left/right eye measures into a single participant-level feature table.

## Data source context

The HPP / Pheno.AI platform documents that researchers access data through a secure Trusted Research Environment and can work in JupyterLab after connecting to a workspace. The platform tutorial also notes that Python packages can be installed inside the environment as needed.

Reference:

- https://knowledgebase.pheno.ai/platform_tutorial.html

## Main operations

1. Load the `fundus` dataset with `PhenoLoader`.
2. Inspect field names and the dataset dictionary.
3. Export the full dataset to `full_fundus.csv`.
4. Remove dataset-specific columns that are not needed for the analysis.
5. Identify matching `*_left` and `*_right` fundus columns.
6. Compute participant-level averages:

```python
df2[base_name] = (df2[left] + df2[right]) / 2
```

7. Drop the original side-specific columns.
8. Save the analytic table as `fundus_avg.csv`.

## Output

- `fundus_avg.csv`: participant-level fundus table used for the later covariate-adjustment and multimodal integration steps.

## File

- `src/01_preprocess_hpp_fundus.py`
