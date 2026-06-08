import os
from typing import Any, Dict, List

import numpy as np
import polars as pl


class DistributionDetector:

    def detect_distribution(
            self,
            file_path: str,
            selected_column: str,
            sample_size: int = 100000
    ) -> Dict[str, Any]:

        if file_path is None or file_path.strip() == "":
            raise ValueError("filePath is required")

        if selected_column is None or selected_column.strip() == "":
            raise ValueError("selectedColumn is required")

        if not os.path.exists(file_path):
            raise ValueError(f"File not found: {file_path}")

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

        sample_size_used = len(
            column_series
        )

        data_type = self._detect_data_type(
            column_series
        )

        null_percentage = self._calculate_null_percentage(
            column_series
        )

        duplicate_percentage = self._calculate_duplicate_percentage(
            column_series
        )

        unique_count = column_series.n_unique()

        sortedness_score = self._calculate_sortedness_score(
            column_series
        )

        reverse_sortedness_score = self._calculate_reverse_sortedness_score(
            column_series
        )

        numeric_stats = self._calculate_numeric_stats(
            column_series
        )

        pattern_result = self._detect_pattern(
            duplicate_percentage=duplicate_percentage,
            skewness=numeric_stats["skewness"],
            sortedness_score=sortedness_score,
            reverse_sortedness_score=reverse_sortedness_score,
            unique_count=unique_count,
            sample_size_used=sample_size_used
        )

        return {
            "rowCount": row_count,
            "sampleSizeUsed": sample_size_used,
            "selectedColumn": selected_column,
            "dataType": data_type,
            "uniqueCount": unique_count,
            "nullPercentage": round(null_percentage, 4),
            "duplicatePercentage": round(duplicate_percentage, 4),
            "minValue": numeric_stats["minValue"],
            "maxValue": numeric_stats["maxValue"],
            "mean": numeric_stats["mean"],
            "median": numeric_stats["median"],
            "standardDeviation": numeric_stats["standardDeviation"],
            "skewness": numeric_stats["skewness"],
            "sortednessScore": round(sortedness_score, 6),
            "reverseSortednessScore": round(reverse_sortedness_score, 6),
            "detectedPattern": pattern_result["detectedPattern"],
            "confidenceScore": pattern_result["confidenceScore"],
            "reason": pattern_result["reason"]
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

    def _detect_data_type(
            self,
            column_series: pl.Series
    ) -> str:

        dtype = column_series.dtype

        if dtype in [
            pl.Int8,
            pl.Int16,
            pl.Int32,
            pl.Int64,
            pl.UInt8,
            pl.UInt16,
            pl.UInt32,
            pl.UInt64,
            pl.Float32,
            pl.Float64
        ]:
            return "NUMERIC"

        if dtype in [
            pl.Date,
            pl.Datetime,
            pl.Time
        ]:
            return "DATETIME"

        return "TEXT"

    def _calculate_null_percentage(
            self,
            column_series: pl.Series
    ) -> float:

        total_count = len(
            column_series
        )

        if total_count == 0:
            return 0.0

        null_count = column_series.null_count()

        return (
                null_count / total_count
        ) * 100

    def _calculate_duplicate_percentage(
            self,
            column_series: pl.Series
    ) -> float:

        total_count = len(
            column_series
        )

        if total_count == 0:
            return 0.0

        unique_count = column_series.n_unique()

        duplicate_count = total_count - unique_count

        return (
                duplicate_count / total_count
        ) * 100

    def _calculate_sortedness_score(
            self,
            column_series: pl.Series
    ) -> float:

        clean_series = column_series.drop_nulls()

        values = clean_series.to_list()

        if len(values) <= 1:
            return 1.0

        sorted_pairs = 0

        total_pairs = len(values) - 1

        for index in range(total_pairs):
            try:
                if values[index] <= values[index + 1]:
                    sorted_pairs += 1
            except Exception:
                continue

        return sorted_pairs / total_pairs

    def _calculate_reverse_sortedness_score(
            self,
            column_series: pl.Series
    ) -> float:

        clean_series = column_series.drop_nulls()

        values = clean_series.to_list()

        if len(values) <= 1:
            return 1.0

        reverse_sorted_pairs = 0

        total_pairs = len(values) - 1

        for index in range(total_pairs):
            try:
                if values[index] >= values[index + 1]:
                    reverse_sorted_pairs += 1
            except Exception:
                continue

        return reverse_sorted_pairs / total_pairs

    def _calculate_numeric_stats(
            self,
            column_series: pl.Series
    ) -> Dict[str, Any]:

        try:

            numeric_series = column_series.cast(
                pl.Float64,
                strict=False
            ).drop_nulls()

            if len(numeric_series) == 0:
                return self._empty_numeric_stats()

            values = numeric_series.to_numpy()

            min_value = float(
                np.min(values)
            )

            max_value = float(
                np.max(values)
            )

            mean_value = float(
                np.mean(values)
            )

            median_value = float(
                np.median(values)
            )

            standard_deviation = float(
                np.std(values)
            )

            skewness_value = self._calculate_skewness(
                values
            )

            return {
                "minValue": round(min_value, 6),
                "maxValue": round(max_value, 6),
                "mean": round(mean_value, 6),
                "median": round(median_value, 6),
                "standardDeviation": round(standard_deviation, 6),
                "skewness": round(skewness_value, 6)
            }

        except Exception:

            return self._empty_numeric_stats()

    def _calculate_skewness(
            self,
            values: np.ndarray
    ) -> float:

        if len(values) < 3:
            return 0.0

        mean_value = np.mean(
            values
        )

        standard_deviation = np.std(
            values
        )

        if standard_deviation == 0:
            return 0.0

        skewness = np.mean(
            ((values - mean_value) / standard_deviation) ** 3
        )

        return float(
            skewness
        )

    def _empty_numeric_stats(
            self
    ) -> Dict[str, Any]:

        return {
            "minValue": None,
            "maxValue": None,
            "mean": None,
            "median": None,
            "standardDeviation": None,
            "skewness": 0.0
        }

    def _detect_pattern(
            self,
            duplicate_percentage: float,
            skewness: float,
            sortedness_score: float,
            reverse_sortedness_score: float,
            unique_count: int,
            sample_size_used: int
    ) -> Dict[str, Any]:

        if duplicate_percentage >= 40:
            return {
                "detectedPattern": "REPEATED_VALUES",
                "confidenceScore": 95.0,
                "reason": "Dataset contains very high duplicate percentage, so repeated values pattern is dominant."
            }

        if reverse_sortedness_score >= 0.95 and sortedness_score <= 0.10:
            return {
                "detectedPattern": "REVERSE_SORTED",
                "confidenceScore": 92.0,
                "reason": "Most adjacent values are in descending order, so reverse sorted pattern is detected."
            }

        if sortedness_score >= 0.95:
            return {
                "detectedPattern": "NEARLY_SORTED",
                "confidenceScore": 90.0,
                "reason": "Most adjacent values are already in ascending order, so nearly sorted pattern is detected."
            }

        if skewness is not None and abs(skewness) >= 1.0:
            return {
                "detectedPattern": "SKEWED",
                "confidenceScore": 88.0,
                "reason": "Skewness value is high, so skewed distribution is detected."
            }

        unique_ratio = 0.0

        if sample_size_used > 0:
            unique_ratio = unique_count / sample_size_used

        if unique_ratio >= 0.80 and abs(skewness) < 0.5 and sortedness_score < 0.80:
            return {
                "detectedPattern": "UNIFORM_RANDOM",
                "confidenceScore": 75.0,
                "reason": "Values are mostly unique, skewness is low, and no strong ordering pattern is present."
            }

        return {
            "detectedPattern": "UNKNOWN",
            "confidenceScore": 50.0,
            "reason": "No strong repeated, skewed, sorted, reverse sorted, or uniform random pattern was detected."
        }