from typing import Optional

from pydantic import BaseModel


class DistributionResponse(BaseModel):

    rowCount: int

    sampleSizeUsed: int

    selectedColumn: str

    dataType: str

    uniqueCount: int

    nullPercentage: float

    duplicatePercentage: float

    minValue: Optional[float] = None

    maxValue: Optional[float] = None

    mean: Optional[float] = None

    median: Optional[float] = None

    standardDeviation: Optional[float] = None

    skewness: Optional[float] = None

    sortednessScore: float

    reverseSortednessScore: float

    detectedPattern: str

    confidenceScore: float

    reason: str