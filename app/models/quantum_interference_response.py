from typing import List

from pydantic import BaseModel


class InterferenceCandidateResponse(BaseModel):

    candidateIndex: int

    candidateValue: float

    partitionImbalance: float

    balanceQuality: float

    beforeAmplitudeWeight: float

    afterAmplitudeWeight: float

    beforeProbability: float

    afterProbability: float

    interferenceType: str

    probabilityChange: float

    selected: bool


class QuantumInterferenceResponse(BaseModel):

    rowCount: int

    sampleSizeUsed: int

    selectedColumn: str

    candidateCount: int

    selectedPivotIndex: int

    selectedPivotValue: float

    constructiveReinforcementCount: int

    destructiveSuppressionCount: int

    interferenceGain: float

    amplitudeConvergenceScore: float

    candidates: List[InterferenceCandidateResponse]

    explanation: str