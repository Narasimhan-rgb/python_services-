from typing import List

from pydantic import BaseModel


class QasmCandidateResponse(BaseModel):

    candidateIndex: int

    candidateValue: float

    partitionImbalance: float

    selectionProbability: float

    rotationAngle: float

    selected: bool


class QuantumQasmResponse(BaseModel):

    rowCount: int

    sampleSizeUsed: int

    selectedColumn: str

    qubitCount: int

    classicalBitCount: int

    selectedPivotIndex: int

    selectedPivotValue: float

    bestPartitionImbalance: float

    circuitPurpose: str

    openQasm: str

    candidates: List[QasmCandidateResponse]

    explanation: str