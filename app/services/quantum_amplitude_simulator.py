import os
from typing import Any, Dict, List

import numpy as np
import polars as pl


class QuantumAmplitudeSimulator:

    def simulate_amplitude(
            self,
            file_path: str,
            selected_column: str,
            sample_size: int = 100000,
            candidate_count: int = 10,
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
                "Quantum amplitude simulation requires a numeric selected column"
            )

        values = numeric_series.to_numpy()

        sample_size_used = len(
            values
        )

        candidate_values = self._generate_candidate_values(
            values=values,
            candidate_count=candidate_count
        )

        candidate_results = self._evaluate_candidates(
            values=values,
            candidate_values=candidate_values,
            learning_rate=learning_rate
        )

        selected_candidate = min(
            candidate_results,
            key=lambda item: item["partitionImbalance"]
        )

        best_partition_imbalance = selected_candidate[
            "partitionImbalance"
        ]

        average_partition_imbalance = float(
            np.mean(
                [
                    candidate["partitionImbalance"]
                    for candidate in candidate_results
                ]
            )
        )

        amplitude_convergence_score = self._calculate_convergence_score(
            average_partition_imbalance
        )

        for candidate in candidate_results:
            candidate["selected"] = (
                    candidate["candidateIndex"]
                    == selected_candidate["candidateIndex"]
            )

        return {
            "rowCount": row_count,
            "sampleSizeUsed": sample_size_used,
            "selectedColumn": selected_column,
            "candidateCount": len(candidate_results),
            "selectedPivotIndex": selected_candidate["candidateIndex"],
            "selectedPivotValue": selected_candidate["candidateValue"],
            "bestPartitionImbalance": round(best_partition_imbalance, 6),
            "averagePartitionImbalance": round(average_partition_imbalance, 6),
            "amplitudeConvergenceScore": round(amplitude_convergence_score, 6),
            "candidates": candidate_results,
            "explanation": "Amplitude simulation assigns higher selection probability to pivot candidates that produce better partition balance."
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
            0.05,
            0.95,
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
                    "candidateValue": round(float(candidate_value), 6),
                    "leftCount": left_count,
                    "rightCount": right_count,
                    "equalCount": equal_count,
                    "partitionImbalance": round(float(partition_imbalance), 6),
                    "amplitudeWeight": float(amplitude_weight),
                    "selectionProbability": 0.0,
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
                candidate["selectionProbability"] = round(
                    uniform_probability,
                    6
                )

                candidate["amplitudeWeight"] = round(
                    candidate["amplitudeWeight"],
                    6
                )

            return raw_candidates

        for candidate in raw_candidates:
            candidate["selectionProbability"] = round(
                candidate["amplitudeWeight"] / total_weight,
                6
            )

            candidate["amplitudeWeight"] = round(
                candidate["amplitudeWeight"],
                6
            )

        return raw_candidates

    def _calculate_convergence_score(
            self,
            average_partition_imbalance: float
    ) -> float:

        distance_from_perfect_balance = abs(
            average_partition_imbalance - 0.5
        )

        score = 1.0 - (
                distance_from_perfect_balance * 2.0
        )

        if score < 0.0:
            return 0.0

        if score > 1.0:
            return 1.0

        return score