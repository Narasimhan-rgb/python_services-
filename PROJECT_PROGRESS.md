# AAQ Python Service Progress

_Last updated: 2026-08-16_

## Completed integrated work

- FastAPI service verified on `127.0.0.1:8000`.
- Dataset profiling supports row/column counts, nulls, duplicates and basic statistics.
- Workload analysis supports skewness, sortedness and distribution/pattern detection.
- The service is used by the Java backend for dataset analysis before AAQ execution.
- Paper V0.4 reproduction support has been integrated into the full project.
- The paper service reads the shared JMH benchmark output (`paper-jmh.csv`) from the benchmark-data workflow.
- The JMH analysis validates the controlled experiment structure and generates measured summaries/figures for the frontend.
- The live paper mode is intentionally separated from normal dataset-upload analysis.

## JMH experiment represented by paper-jmh.csv

```text
6 algorithms × 15 distributions × 5 sizes × 30 seeds = 13,500 measurements
```

The controlled input sizes are:

```text
1,000
10,000
100,000
500,000
1,000,000
```

The paper-analysis workflow computes measured comparisons from the JMH result CSV and supports the Paper V0.4 frontend view.

## Data used / source

Published dataset source:

- Kaggle: https://www.kaggle.com/datasets/narasimhandasarathy/quantum-amplititude-sort-testing-data/data

The project combines controlled synthetic workloads with open-source/publicly available data for realistic evaluation. Open Library / Internet Archive catalogue data is used where applicable as real-world source material.

## Service relationship

```text
AAQ_frontend
     ↓
AAQalgorithim (Java backend)
     ↓
python_services- (profiling + paper analysis)
```

## Reproducibility rule

Exact research-result reproduction is based on `paper-jmh.csv` generated from the controlled JMH matrix. User-uploaded datasets are kept as a separate application/demo evaluation path and should not be expected to reproduce the exact JMH timing values.
