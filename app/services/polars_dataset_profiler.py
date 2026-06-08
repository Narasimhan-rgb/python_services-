import os
from typing import Any, Dict

import numpy as np
import polars as pl


class PolarsDatasetProfiler:

    def profile_dataset(
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

        dataframe = self._read_file(file_path)

        if selected_column not in dataframe.columns:
            raise ValueError(
                f"Selected column '{selected_column}' not found. Available columns: {dataframe.columns}"
            )

        row_count = dataframe.height
        column_count = dataframe.width

        if row_count == 0:
            raise ValueError("Dataset is empty")

        sample_dataframe = dataframe

        if row_count > sample_size:
            sample_dataframe = dataframe.head(sample_size)

        column_series = sample_dataframe[selected_column]

        data_type = self._detect_data_type(column_series)

        null_percentage = self._calculate_null_percentage(column_series)

        duplicate_percentage = self._calculate_duplicate_percentage(column_series)

        sortedness_score = self._calculate_sortedness_score(column_series)

        numeric_stats = self._calculate_numeric_stats(column_series)

        detected_pattern = self._detect_pattern(
            duplicate_percentage=duplicate_percentage,
            skewness=numeric_stats["skewness"],
            sortedness_score=sortedness_score
        )

        return {
            "rowCount": row_count,
            "columnCount": column_count,
            "selectedColumn": selected_column,
            "dataType": data_type,
            "nullPercentage": round(null_percentage, 4),
            "duplicatePercentage": round(duplicate_percentage, 4),
            "minValue": numeric_stats["minValue"],
            "maxValue": numeric_stats["maxValue"],
            "mean": numeric_stats["mean"],
            "median": numeric_stats["median"],
            "standardDeviation": numeric_stats["standardDeviation"],
            "skewness": numeric_stats["skewness"],
            "sortednessScore": round(sortedness_score, 6),
            "detectedPattern": detected_pattern
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

        total_count = len(column_series)

        if total_count == 0:
            return 0.0

        null_count = column_series.null_count()

        return (null_count / total_count) * 100

    def _calculate_duplicate_percentage(
            self,
            column_series: pl.Series
    ) -> float:

        total_count = len(column_series)

        if total_count == 0:
            return 0.0

        unique_count = column_series.n_unique()

        duplicate_count = total_count - unique_count

        return (duplicate_count / total_count) * 100

    def _calculate_sortedness_score(
            self,
            column_series: pl.Series
    ) -> float:

        clean_series = column_series.drop_nulls()

        values = clean_series.to_list()

        total_pairs = len(values) - 1

        if total_pairs <= 0:
            return 1.0

        sorted_pairs = 0

        for index in range(total_pairs):
            try:
                if values[index] <= values[index + 1]:
                    sorted_pairs += 1
            except Exception:
                continue

        return sorted_pairs / total_pairs

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

            min_value = float(np.min(values))
            max_value = float(np.max(values))
            mean_value = float(np.mean(values))
            median_value = float(np.median(values))
            standard_deviation = float(np.std(values))

            skewness_value = self._calculate_skewness(values)

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

        mean_value = np.mean(values)
        standard_deviation = np.std(values)

        if standard_deviation == 0:
            return 0.0

        skewness = np.mean(
            ((values - mean_value) / standard_deviation) ** 3
        )

        return float(skewness)

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
            sortedness_score: float
    ) -> str:

        if duplicate_percentage >= 40:
            return "REPEATED_VALUES"

        if skewness is not None and abs(skewness) >= 1.0:
            return "SKEWED"

        if sortedness_score >= 0.95:
            return "NEARLY_SORTED"

        if sortedness_score <= 0.05:
            return "REVERSE_SORTED"

        return "UNKNOWN"