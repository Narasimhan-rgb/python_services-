# AAQ Python Analysis Service

> FastAPI-based research-support service for Adaptive Amplitude QuickSort (AAQ), focused on dataset profiling, pattern detection, and benchmark-support analytics.

## Purpose

This service supports the AAQ research platform by analysing uploaded datasets before benchmarking. It helps identify dataset characteristics that may affect sorting behaviour.

## What this service does

- Reads structured dataset files
- Detects row and column counts
- Calculates null and duplicate percentages
- Computes basic descriptive statistics
- Estimates sortedness and skewness indicators
- Detects dataset patterns for benchmark interpretation
- Provides API responses for the Java backend and React dashboard

## Scope note

This service is part of a **classical quantum-inspired algorithm research project**. Any amplitude or interference-style outputs are research visualisations or simulation-style indicators, not proof of real quantum speedup.

## Technology stack

| Area | Tools |
|---|---|
| API | FastAPI |
| Runtime | Python |
| Data processing | Polars, NumPy, SciPy |
| Server | Uvicorn |
| Validation | Pydantic |

## Local setup

```cmd
git clone https://github.com/Narasimhan-rgb/python_services-.git
cd python_services-
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

## API role in AAQ platform

```text
Dataset file
→ Python analysis service
→ dataset profile and pattern metrics
→ AAQ backend benchmark flow
→ dashboard and report output
```

## MS portfolio value

This repository shows backend API design, data-analysis services, and research-system engineering for an algorithmic project.

## Roadmap

- Rename repository to `aaq-python-analysis-service`
- Add endpoint documentation with sample requests and responses
- Add unit tests for dataset profiling logic
- Add sample CSV file for demo use
- Add Docker or simple deployment instructions
