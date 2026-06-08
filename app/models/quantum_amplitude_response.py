from typing import List

from pydantic import BaseModel


class PivotCandidateResponse(BaseModel):

    candidateIndex: int

    candidateValue: float

    leftCount: int

    rightCount: int

    equalCount: int

    partitionImbalance: float

    amplitudeWeight: float

    selectionProbability: float

    selected: bool


class QuantumAmplitudeResponse(BaseModel):

    rowCount: int

    sampleSizeUsed: int

    selectedColumn: str

    candidateCount: int

    selectedPivotIndex: int

    selectedPivotValue: float

    bestPartitionImbalance: float

    averagePartitionImbalance: float

    amplitudeConvergenceScore: float

    candidates: List[PivotCandidateResponse]

    explanation: str