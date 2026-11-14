# ResQNet dataset guide

## Included dataset

`data/ResQNet_Incident_Dataset.xlsx` contains 6,480 synthetic incident-report rows across 9 categories and 3 languages (English, Hindi and Telugu). It has Train (4,536), Validation (864), Test (1,080), All_Data, Split_Summary and Data_Dictionary sheets.

Equivalent UTF-8 CSV files are included: `train_reports.csv`, `validation_reports.csv`, `test_reports.csv`, and `training_reports.csv` (all rows). The baseline trainer uses only `train_reports.csv`; the evaluation script trains on Train and reports metrics on the untouched Test partition.

## Important data-quality warning

Every row is synthetic and generated from templates. The dataset is useful for learning the training/evaluation workflow and demonstrating the prototype, but it is not a real emergency dataset, not independently verified, and not a valid basis for claims about real-world performance. Some Hindi and Telugu phrasing may need correction by fluent native speakers. The event-group split keeps variations of one simulated scenario in one partition, reducing direct near-duplicate leakage. However, all partitions come from the same synthetic generation process, so test results still do not establish generalization to real incidents.

## Suggested workflow

1. Inspect the Excel workbook and `Split_Summary`.
2. Train using `python scripts/train_baseline.py` (train partition only).
3. Evaluate using `python scripts/evaluate_baseline.py` (held-out test partition).
4. In Colab, run `notebooks/ResQNet_Colab_Training.ipynb`; it uses the same fixed CSV splits.
5. For a meaningful study, collect permissioned, anonymized reports; document source and licence; get fluent-speaker annotation; and create a new source/event-held-out test set.
