# AAQ Python Analysis Service

> **AAQ component repository.** The canonical project entry point is [AAQalgorithim](https://github.com/Narasimhan-rgb/AAQalgorithim), which groups this service with the Java backend and React frontend.

FastAPI-based research-support service for Adaptive Amplitude QuickSort (AAQ), focused on dataset profiling, workload detection, quantum-inspired simulation support, and research/reproducibility analysis.

## Role in the AAQ platform

```text
Raw dataset
→ Python profiling / pattern analysis
→ Java AAQ execution
→ benchmark persistence

JMH output
→ Python analysis
→ measured summaries / figures
→ Java API
→ React dashboard
```

## Technology

- Python 3
- FastAPI + Uvicorn
- Pydantic
- Polars / NumPy / SciPy
- SQLAlchemy for local development storage

## Local setup

When cloning the complete AAQ system, prefer:

```bash
git clone --recurse-submodules https://github.com/Narasimhan-rgb/AAQalgorithim.git
cd AAQalgorithim/python-service
```

Or clone this component directly:

```bash
git clone https://github.com/Narasimhan-rgb/python_services-.git
cd python_services-
```

Then:

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API docs are available at `http://127.0.0.1:8000/docs`.

## Repository hygiene

Local SQLite databases, datasets, generated reports, environment files, and Python caches are intentionally ignored. Do not commit user data or secrets.

## Scope note

This service belongs to a **classical quantum-inspired algorithm** project. Simulation or amplitude-style outputs are classical research artefacts and are not claims of quantum-hardware execution or universal quantum speedup.
