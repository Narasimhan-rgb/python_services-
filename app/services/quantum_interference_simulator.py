import os
from typing import Any, Dict, List

import numpy as np
import polars as pl


class QuantumInterferenceSimulator:

    def simulate_interference(
            self,
            file_path: str,
            selected_column: str,
            sample_size: int = 100000,
            candidate_count: int = 10,
            learning_rate: float = 0.1,
            reinforcement_strength: float = 1.25,
            suppression_strength: float = 0.75
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
                "Quantum interference simulation requires a numeric selected column"
            )

        values = numeric_series.to_numpy()

        sample_size_used = len(
            values
        )

        candidate_values = self._generate_candidate_values(
            values=values,
            candidate_count=candidate_count
        )

        initial_candidates = self._build_initial_candidates(
            values=values,
            candidate_values=candidate_values,
            learning_rate=learning_rate
        )

        before_total_weight = sum(
            candidate["beforeAmplitudeWeight"]
            for candidate in initial_candidates
        )

        for candidate in initial_candidates:
            candidate["beforeProbability"] = candidate["beforeAmplitudeWeight"] / before_total_weight

        selected_candidate = min(
            initial_candidates,
            key=lambda item: item["partitionImbalance"]
        )

        updated_candidates = self._apply_interference(
            candidates=initial_candidates,
            selected_candidate=selected_candidate,
            reinforcement_strength=reinforcement_strength,
            suppression_strength=suppression_strength
        )

        after_total_weight = sum(
            candidate["afterAmplitudeWeight"]
            for candidate in updated_candidates
        )

        for candidate in updated_candidates:
            candidate["afterProbability"] = candidate["afterAmplitudeWeight"] / after_total_weight
            candidate["probabilityChange"] = candidate["afterProbability"] - candidate["beforeProbability"]
            candidate["selected"] = candidate["candidateIndex"] == selected_candidate["candidateIndex"]

        constructive_reinforcement_count = sum(
            1
            for candidate in updated_candidates
            if candidate["interferenceType"] == "CONSTRUCTIVE_REINFORCEMENT"
        )

        destructive_suppression_count = sum(
            1
            for candidate in updated_candidates
            if candidate["interferenceType"] == "DESTRUCTIVE_SUPPRESSION"
        )

        selected_before_probability = selected_candidate["beforeProbability"]

        selected_after_probability = 0.0

        for candidate in updated_candidates:
            if candidate["candidateIndex"] == selected_candidate["candidateIndex"]:
                selected_after_probability = candidate["afterProbability"]
                break

        interference_gain = selected_after_probability - selected_before_probability

        average_after_imbalance = float(
            np.average(
                [
                    candidate["partitionImbalance"]
                    for candidate in updated_candidates
                ],
                weights=[
                    candidate["afterProbability"]
                    for candidate in updated_candidates
                ]
            )
        )

        amplitude_convergence_score = self._calculate_convergence_score(
            average_after_imbalance
        )

        cleaned_candidates = []

        for candidate in updated_candidates:
            cleaned_candidates.append(
                {
                    "candidateIndex": candidate["candidateIndex"],
                    "candidateValue": round(candidate["candidateValue"], 6),
                    "partitionImbalance": round(candidate["partitionImbalance"], 6),
                    "balanceQuality": round(candidate["balanceQuality"], 6),
                    "beforeAmplitudeWeight": round(candidate["beforeAmplitudeWeight"], 6),
                    "afterAmplitudeWeight": round(candidate["afterAmplitudeWeight"], 6),
                    "beforeProbability": round(candidate["beforeProbability"], 6),
                    "afterProbability": round(candidate["afterProbability"], 6),
                    "interferenceType": candidate["interferenceType"],
                    "probabilityChange": round(candidate["probabilityChange"], 6),
                    "selected": candidate["selected"]
                }
            )

        return {
            "rowCount": row_count,
            "sampleSizeUsed": sample_size_used,
            "selectedColumn": selected_column,
            "candidateCount": len(cleaned_candidates),
            "selectedPivotIndex": selected_candidate["candidateIndex"],
            "selectedPivotValue": round(selected_candidate["candidateValue"], 6),
            "constructiveReinforcementCount": constructive_reinforcement_count,
            "destructiveSuppressionCount": destructive_suppression_count,
            "interferenceGain": round(float(interference_gain), 6),
            "amplitudeConvergenceScore": round(float(amplitude_convergence_score), 6),
            "candidates": cleaned_candidates,
            "explanation": "Quantum interference simulation reinforces balanced pivot candidates and suppresses imbalanced pivot candidates."
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

    def _build_initial_candidates(
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

        candidates = []

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

            before_amplitude_weight = np.exp(
                learning_rate * 10.0 * balance_quality
            ) * np.exp(
                -distance_from_median
            )

            candidates.append(
                {
                    "candidateIndex": index,
                    "candidateValue": float(candidate_value),
                    "partitionImbalance": float(partition_imbalance),
                    "balanceQuality": float(balance_quality),
                    "beforeAmplitudeWeight": float(before_amplitude_weight),
                    "afterAmplitudeWeight": float(before_amplitude_weight),
                    "beforeProbability": 0.0,
                    "afterProbability": 0.0,
                    "interferenceType": "NEUTRAL",
                    "probabilityChange": 0.0,
                    "selected": False
                }
            )

        return candidates

    def _apply_interference(
            self,
            candidates: List[Dict[str, Any]],
            selected_candidate: Dict[str, Any],
            reinforcement_strength: float,
            suppression_strength: float
    ) -> List[Dict[str, Any]]:

        selected_index = selected_candidate[
            "candidateIndex"
        ]

        for candidate in candidates:

            distance_from_selected = abs(
                candidate["candidateIndex"] - selected_index
            )

            neighbor_factor = 1.0 / (
                    1.0 + distance_from_selected
            )

            if candidate["partitionImbalance"] <= 0.65:

                reinforcement_multiplier = 1.0 + (
                        (
                                reinforcement_strength - 1.0
                        ) * neighbor_factor
                )

                candidate["afterAmplitudeWeight"] = (
                        candidate["beforeAmplitudeWeight"]
                        * reinforcement_multiplier
                )

                candidate["interferenceType"] = "CONSTRUCTIVE_REINFORCEMENT"

            elif candidate["partitionImbalance"] >= 0.80:

                suppression_multiplier = 1.0 - (
                        (
                                1.0 - suppression_strength
                        ) * neighbor_factor
                )

                if suppression_multiplier < 0.1:
                    suppression_multiplier = 0.1

                candidate["afterAmplitudeWeight"] = (
                        candidate["beforeAmplitudeWeight"]
                        * suppression_multiplier
                )

                candidate["interferenceType"] = "DESTRUCTIVE_SUPPRESSION"

            else:

                candidate["afterAmplitudeWeight"] = candidate["beforeAmplitudeWeight"]
                candidate["interferenceType"] = "NEUTRAL"

        return candidates

    def _calculate_convergence_score(
            self,
            weighted_average_partition_imbalance: float
    ) -> float:

        distance_from_perfect_balance = abs(
            weighted_average_partition_imbalance - 0.5
        )

        score = 1.0 - (
                distance_from_perfect_balance * 2.0
        )

        if score < 0.0:
            return 0.0

        if score > 1.0:
            return 1.0

        return score