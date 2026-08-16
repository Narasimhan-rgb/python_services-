# AAQ Python Analysis Service

> FastAPI-based research-support service for Adaptive Amplitude QuickSort (AAQ), focused on dataset profiling, workload detection, JMH result analysis, and Paper V0.4 reproducibility support.

## Purpose

This service supports the AAQ research platform by analysing uploaded datasets before benchmarking and by processing the controlled JMH results used for paper reproduction.

## Current integrated project status

The integrated service now supports:

- FastAPI service on port `8000`
- large dataset profiling with Polars
- row and column counting
- null and duplicate percentage calculation
- descriptive statistics
- skewness and sortedness analysis
- dataset-pattern/distribution detection
- quantum-inspired explanation/simulation support
- Paper V0.4 reference-result support
- live JMH analysis from `paper-jmh.csv`
- validation of the 13,500-row benchmark matrix
- measured one-million-record comparisons
- figure generation for paper/reproducibility views
- Java backend integration through `/paper/...` endpoints

## Paper benchmark / reproducibility

The controlled research benchmark contains:

```text
6 algorithms
15 distributions
5 input sizes
30 independent seeds
= 13,500 measured rows
```

The combined result file is `paper-jmh.csv`. In the integrated project, the paper reproduction service expects it under the shared `benchmark-data` directory and analyses the measured JMH output rather than treating it as a normal input dataset.

## Data used / source

The research uses a combination of controlled synthetic workloads and publicly available/open-source data.

**Published dataset source:**

- Kaggle — [Quantum Amplititude Sort Testing Data](https://www.kaggle.com/datasets/narasimhandasarathy/quantum-amplititude-sort-testing-data/data)

Synthetic workloads are generated deterministically using workload type, input size and seed so the same data instance can be supplied to each competing sorting algorithm. Workload patterns include random, skewed/Gaussian, Zipf-like, nearly sorted, reverse sorted, repeated-value, bounded-integer, streaming and high-entropy cases.

Open Library / Internet Archive catalogue data is also used as real-world source material where applicable.

## Scope note

This service is part of a **classical quantum-inspired algorithm research project**. Any amplitude or interference-style outputs are classical research visualisations/indicators. They are not evidence of execution on quantum hardware or a universal quantum speedup.

## Technology stack

| Area | Tools |
|---|---|
| API | FastAPI |
| Runtime | Python 3 |
| Data processing | Polars, NumPy, SciPy |
| Paper/JMH analysis | Python analysis scripts and generated figures |
| Server | Uvicorn |
| Validation | Pydantic |

## Local setup

```cmd
git clone https://github.com/Narasimhan-rgb/python_services-.git
cd python_services-
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Role in the AAQ platform

```text
Raw dataset
→ Python profiling / pattern analysis
→ Java AAQ execution
→ benchmark persistence

paper-jmh.csv
→ Python JMH analysis
→ measured paper summary + figures
→ Java paper API
→ React Paper V0.4 page
```

## Related repositories

- `AAQalgorithim` — Java backend, AAQ algorithm and JMH benchmark engine
- `AAQ_frontend` — dashboard, live AAQ graphs and Paper V0.4 reproduction UI

## Progress documentation

See [`PROJECT_PROGRESS.md`](PROJECT_PROGRESS.md) for the latest integrated-service status and reproducibility work.
