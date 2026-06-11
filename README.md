# AAQ Python Service

## Enterprise Quantum-Inspired Adaptive Sorting Optimization Platform

## Proposed Algorithm

Adaptive Amplitude QuickSort - AAQ

---

## 1. Python Service Overview

This is the Python FastAPI service for the **Enterprise Quantum-Inspired Adaptive Sorting Optimization Platform**.

The Python service supports the Java backend by handling:

```text
Large dataset profiling
Dataset pattern detection
Statistical analysis
Amplitude simulation
Interference simulation
OpenQASM generation
Qiskit circuit generation
```

The main sorting algorithm, **Adaptive Amplitude QuickSort**, runs in the Java backend.

The Python service is used for dataset profiling and quantum-inspired research visualization support.

---

## 2. Technology Stack

```text
Python
FastAPI
Polars
NumPy
SciPy
Qiskit
Uvicorn
Pydantic
```

---

## 3. Main Responsibilities

The Python service performs:

```text
Read dataset file
Analyze selected column
Calculate row count
Calculate column count
Calculate null percentage
Calculate duplicate percentage
Calculate minimum value
Calculate maximum value
Calculate mean
Calculate median
Calculate standard deviation
Calculate skewness
Calculate sortedness score
Detect dataset pattern
Simulate amplitude probability
Simulate interference update
Generate OpenQASM
Generate Qiskit circuit
```

---

## 4. API Base URL

```text
http://localhost:8000
```

---

## 5. Available APIs

```text
GET  /health
POST /profile/dataset
POST /detect/distribution
POST /quantum/amplitude-simulate
POST /quantum/interference-simulate
POST /quantum/generate-qasm
POST /quantum/qiskit-circuit
```

---

## 6. Health API

```text
GET /health
```

Expected response:

```json
{
  "status": "UP",
  "service": "python-service"
}
```

This API is used by the backend and frontend system status page to confirm that the Python service is running.

---

## 7. Dataset Profiling API

```text
POST /profile/dataset
```

This API receives a dataset file path and selected column.

It returns:

```text
Row count
Column count
Selected column
Data type
Null percentage
Duplicate percentage
Minimum value
Maximum value
Mean
Median
Standard deviation
Skewness
Sortedness score
Detected pattern
```

The Java backend stores this result in PostgreSQL.

---

## 8. Dataset Pattern Detection

The Python service detects dataset patterns such as:

```text
UNIFORM_RANDOM
SKEWED
NEARLY_SORTED
REVERSE_SORTED
REPEATED_VALUES
ADVERSARIAL
ZIPF_DISTRIBUTION
UNKNOWN
```

This pattern is used by:

```text
AAQ analysis
Recommendation engine
Benchmark explanation
Report generation
```

---

## 9. Quantum-Inspired Simulation APIs

The Python service provides quantum-inspired visualization support.

## Amplitude Simulation

```text
POST /quantum/amplitude-simulate
```

This simulates pivot candidate probability.

It helps explain:

```text
Amplitude weights
Pivot candidate probability
Selected pivot candidate
Amplitude convergence
```

## Interference Simulation

```text
POST /quantum/interference-simulate
```

This simulates:

```text
Constructive reinforcement
Destructive suppression
Good pivot strengthening
Poor pivot suppression
```

## OpenQASM Generation

```text
POST /quantum/generate-qasm
```

This generates OpenQASM-style representation for research explanation.

## Qiskit Circuit Generation

```text
POST /quantum/qiskit-circuit
```

This generates Qiskit-style circuit output for visual explanation.

---

## 10. Important Note About Quantum

This project does not run on real quantum hardware.

The Python service provides quantum-inspired simulation only.

The quantum-inspired concepts are:

```text
Amplitude probability
Pivot candidate weighting
Constructive reinforcement
Destructive suppression
Neighbor correlation
OpenQASM representation
Qiskit circuit explanation
```

The actual AAQ sorting engine is implemented in Java.

---

## 11. How to Run Python Service

Open terminal inside the Python service folder:

```bash
cd "D:\AJVRPS TECH\researchpaper\papers\processing papers\Quantum-Inspired Sorting Algorithmsog\python-service"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run service:

```bash
uvicorn main:app --reload --port 8000
```

Python service will run on:

```text
http://localhost:8000
```

---

## 12. Required Before Running

Make sure Python dependencies are installed.

Required packages:

```text
fastapi
uvicorn
polars
numpy
scipy
qiskit
pydantic
python-multipart
```

---

## 13. Connection With Java Backend

The React frontend does not directly depend on Python service for most operations.

The flow is:

```text
React Frontend
        ↓
Java Spring Boot Backend
        ↓
Python FastAPI Service
```

The Java backend calls Python service for:

```text
Dataset profiling
Distribution detection
Amplitude simulation
Interference simulation
OpenQASM generation
Qiskit circuit generation
```

---

## 14. Demo Flow Involving Python Service

During demo, the Python service is used when:

```text
Analyze Dataset button is clicked
Quantum amplitude simulation is run
Interference simulation is run
OpenQASM is generated
Qiskit circuit is generated
System status checks Python connection
```

---

## 15. Known Limitations

```text
Python service must be running separately
Large XLSX files may take time to analyze
Results depend on dataset size and selected column
This service does not execute real quantum hardware
This service supports AAQ explanation, not the main sorting engine
```

---

## 16. Final Python Service Deliverables

```text
FastAPI service
Health endpoint
Dataset profiling endpoint
Pattern detection endpoint
Amplitude simulation endpoint
Interference simulation endpoint
OpenQASM generation endpoint
Qiskit circuit generation endpoint
Backend integration support
System status support
```

---

## 17. Project Conclusion

This Python service successfully supports the **Enterprise Quantum-Inspired Adaptive Sorting Optimization Platform** by providing dataset profiling, statistical analysis, pattern detection, and quantum-inspired visualization support.

It works together with the Java backend and React frontend to demonstrate the proposed **Adaptive Amplitude QuickSort** algorithm.