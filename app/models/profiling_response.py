from typing import Optional

from pydantic import BaseModel


class ProfilingResponse(BaseModel):

    rowCount: int

    columnCount: int

    selectedColumn: str

    dataType: str

    nullPercentage: float

    duplicatePercentage: float

    minValue: Optional[float] = None

    maxValue: Optional[float] = None

    mean: Optional[float] = None

    median: Optional[float] = None

    standardDeviation: Optional[float] = None

    skewness: Optional[float] = None

    sortednessScore: float

    detectedPattern: str