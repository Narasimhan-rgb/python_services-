# Repository status — 22 September 2026

## Role

FastAPI dataset profiling, distribution detection, quantum simulations and measured JMH CSV analysis. This is one component of AAQ, not a separate finished research paper.

## Reproduction

`python -m venv .venv`, activate it, then `pip install -r requirements.txt`. Run `python -m uvicorn main:app --host 127.0.0.1 --port 8000`. Docs: http://127.0.0.1:8000/docs. Run `python -m unittest discover -s tests -v`.

## Outstanding work

Set AAQ_JWT_SECRET in your shell to preserve sessions across restarts; otherwise a process-local random key is used. Profiling accepts local filesystem paths and is intended for loopback use only. Independent research measurements and a controlled JMH runner remain required.

Build or unit-test success is not evidence of a deployed service or a completed research evaluation. See the pull request for checks executed for this revision.

## Checks executed in this pass

Six CSV-analysis unit tests passed. FastAPI health, valid CSV upload and invalid CSV rejection passed through TestClient. Full dataset profiling and database integration were not exercised.
