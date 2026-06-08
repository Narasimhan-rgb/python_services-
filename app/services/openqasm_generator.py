import os
from typing import Any, Dict, List

import numpy as np
import polars as pl


class OpenQasmGenerator:

    def generate_qasm(
            self,
            file_path: str,
            selected_column: str,
            sample_size: int = 100000,
            candidate_count: int = 5,
            learning_rate: float = 0.1
    ) -> Dict[str, Any]:

        if file_path is None or file_path.strip() == "":
            raise ValueError("filePath is required")

        if selected_column is None or selected_column.strip() == "":
            raise ValueError("selectedColumn is required")

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

        if candidate_count < 3:
            candidate_count = 3

        if candidate_count > 8:
            candidate_count = 8

        dataframe = self._read_file(
            file_path
        )

        if selected_column not in dataframe.columns:
            raise ValueError(
                f"Selected column '{selected_column}' not found. Available columns: {dataframe.columns}"
            )

        row_count = dataframe.height

        if row_count == 0:
            raise ValueError("Dataset is empty")

        sample_dataframe = dataframe

        if row_count > sample_size:
            sample_dataframe = dataframe.head(
                sample_size
            )

        column_series = sample_dataframe[
            selected_column
        ]

        numeric_series = column_series.cast(
            pl.Float64,
            strict=False
        ).drop_nulls()

        if len(numeric_series) == 0:
            raise ValueError(
                "OpenQASM generation requires a numeric selected column"
            )

        values = numeric_series.to_numpy()

        sample_size_used = len(
            values
        )

        candidate_values = self._generate_candidate_values(
            values=values,
            candidate_count=candidate_count
        )

        candidates = self._evaluate_candidates(
            values=values,
            candidate_values=candidate_values,
            learning_rate=learning_rate
        )

        selected_candidate = min(
            candidates,
            key=lambda item: item["partitionImbalance"]
        )

        for candidate in candidates:
            candidate["selected"] = (
                    candidate["candidateIndex"]
                    == selected_candidate["candidateIndex"]
            )

            candidate["rotationAngle"] = self._probability_to_rotation_angle(
                candidate["selectionProbability"]
            )

        open_qasm = self._build_openqasm(
            candidates=candidates
        )

        cleaned_candidates = []

        for candidate in candidates:
            cleaned_candidates.append(
                {
                    "candidateIndex": candidate["candidateIndex"],
                    "candidateValue": round(candidate["candidateValue"], 6),
                    "partitionImbalance": round(candidate["partitionImbalance"], 6),
                    "selectionProbability": round(candidate["selectionProbability"], 6),
                    "rotationAngle": round(candidate["rotationAngle"], 6),
                    "selected": candidate["selected"]
                }
            )

        return {
            "rowCount": row_count,
            "sampleSizeUsed": sample_size_used,
            "selectedColumn": selected_column,
            "qubitCount": len(candidates),
            "classicalBitCount": len(candidates),
            "selectedPivotIndex": selected_candidate["candidateIndex"],
            "selectedPivotValue": round(selected_candidate["candidateValue"], 6),
            "bestPartitionImbalance": round(selected_candidate["partitionImbalance"], 6),
            "circuitPurpose": "OpenQASM explanation circuit for AAQ amplitude-weighted pivot candidate probabilities.",
            "openQasm": open_qasm,
            "candidates": cleaned_candidates,
            "explanation": "Each qubit represents one pivot candidate. Higher probability candidates receive stronger rotation angles, and neighbor CX gates represent entanglement-inspired candidate correlation."
        }

    def _read_file(
            self,
            file_path: str
    ) -> pl.DataFrame:

        lower_path = file_path.lower()

        if lower_path.endswith(".csv"):
            return pl.read_csv(
                file_path,
                infer_schema_length=10000,
                ignore_errors=True
            )

        if lower_path.endswith(".xlsx") or lower_path.endswith(".xls"):
            return pl.read_excel(
                file_path
            )

        if lower_path.endswith(".parquet"):
            return pl.read_parquet(
                file_path
            )

        raise ValueError(
            "Unsupported file type. Supported types: CSV, XLSX, XLS, PARQUET"
        )

    def _generate_candidate_values(
            self,
            values: np.ndarray,
            candidate_count: int
    ) -> List[float]:

        unique_values = np.unique(
            values
        )

        if len(unique_values) <= candidate_count:
            return [
                float(value)
                for value in unique_values
            ]

        quantiles = np.linspace(
            0.10,
            0.90,
            candidate_count
        )

        candidate_values = []

        for quantile in quantiles:

            candidate_value = float(
                np.quantile(
                    values,
                    quantile
                )
            )

            candidate_values.append(
                candidate_value
            )

        cleaned_candidates = []

        for value in candidate_values:
            if value not in cleaned_candidates:
                cleaned_candidates.append(
                    value
                )

        return cleaned_candidates

    def _evaluate_candidates(
            self,
            values: np.ndarray,
            candidate_values: List[float],
            learning_rate: float
    ) -> List[Dict[str, Any]]:

        total_count = len(
            values
        )

        median_value = float(
            np.median(
                values
            )
        )

        standard_deviation = float(
            np.std(
                values
            )
        )

        if standard_deviation == 0:
            standard_deviation = 1.0

        raw_candidates = []

        for index, candidate_value in enumerate(candidate_values):

            left_count = int(
                np.sum(
                    values < candidate_value
                )
            )

            right_count = int(
                np.sum(
                    values > candidate_value
                )
            )

            equal_count = int(
                np.sum(
                    values == candidate_value
                )
            )

            left_effective = left_count + (
                    equal_count / 2.0
            )

            right_effective = right_count + (
                    equal_count / 2.0
            )

            partition_imbalance = max(
                left_effective,
                right_effective
            ) / total_count

            balance_quality = 1.0 - (
                    (
                            partition_imbalance - 0.5
                    ) * 2.0
            )

            if balance_quality < 0.0:
                balance_quality = 0.0

            distance_from_median = abs(
                candidate_value - median_value
            ) / standard_deviation

            amplitude_weight = np.exp(
                learning_rate * 10.0 * balance_quality
            ) * np.exp(
                -distance_from_median
            )

            raw_candidates.append(
                {
                    "candidateIndex": index,
                    "candidateValue": float(candidate_value),
                    "partitionImbalance": float(partition_imbalance),
                    "amplitudeWeight": float(amplitude_weight),
                    "selectionProbability": 0.0,
                    "rotationAngle": 0.0,
                    "selected": False
                }
            )

        total_weight = sum(
            candidate["amplitudeWeight"]
            for candidate in raw_candidates
        )

        if total_weight <= 0:
            uniform_probability = 1.0 / len(
                raw_candidates
            )

            for candidate in raw_candidates:
                candidate["selectionProbability"] = uniform_probability

            return raw_candidates

        for candidate in raw_candidates:
            candidate["selectionProbability"] = (
                    candidate["amplitudeWeight"] / total_weight
            )

        return raw_candidates

    def _probability_to_rotation_angle(
            self,
            probability: float
    ) -> float:

        if probability < 0.0:
            probability = 0.0

        if probability > 1.0:
            probability = 1.0

        angle = 2.0 * np.arcsin(
            np.sqrt(
                probability
            )
        )

        return float(
            angle
        )

    def _build_openqasm(
            self,
            candidates: List[Dict[str, Any]]
    ) -> str:

        qubit_count = len(
            candidates
        )

        lines = []

        lines.append("OPENQASM 2.0;")
        lines.append('include "qelib1.inc";')
        lines.append("")
        lines.append("// AAQ Quantum-Inspired Pivot Candidate Explanation Circuit")
        lines.append("// Each qubit represents one pivot candidate.")
        lines.append("// H gates create superposition-inspired candidate space.")
        lines.append("// RY rotations encode amplitude-weighted selection probabilities.")
        lines.append("// CX gates represent entanglement-inspired neighbor correlation.")
        lines.append("")
        lines.append(f"qreg q[{qubit_count}];")
        lines.append(f"creg c[{qubit_count}];")
        lines.append("")

        lines.append("// Step 1: Superposition-inspired candidate space")
        for index in range(qubit_count):
            lines.append(f"h q[{index}];")

        lines.append("")
        lines.append("// Step 2: Amplitude-weighted probability encoding")
        for candidate in candidates:
            index = candidate["candidateIndex"]
            angle = round(
                candidate["rotationAngle"],
                6
            )

            lines.append(
                f"ry({angle}) q[{index}];"
            )

        lines.append("")
        lines.append("// Step 3: Entanglement-inspired neighbor correlation")
        for index in range(qubit_count - 1):
            lines.append(
                f"cx q[{index}], q[{index + 1}];"
            )

        lines.append("")
        lines.append("// Step 4: Measure candidate states")
        for index in range(qubit_count):
            lines.append(
                f"measure q[{index}] -> c[{index}];"
            )

        return "\n".join(
            lines
        )