from typing import List

from pydantic import BaseModel


class QiskitCandidateResponse(BaseModel):

    candidateIndex: int
    candidateValue: float
    partitionImbalance: float
    selectionProbability: float
    rotationAngle: float
    selected: bool


class QiskitCircuitResponse(BaseModel):

    rowCount: int
    sampleSizeUsed: int
    selectedColumn: str

    qubitCount: int
    classicalBitCount: int
    circuitDepth: int

    selectedPivotIndex: int
    selectedPivotValue: float
    bestPartitionImbalance: float

    qiskitCircuitText: str
    openQasm: str

    candidates: List[QiskitCandidateResponse]

    explanation: str