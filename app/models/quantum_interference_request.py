from pydantic import BaseModel


class QuantumInterferenceRequest(BaseModel):

    filePath: str

    selectedColumn: str

    sampleSize: int = 100000

    candidateCount: int = 10

    learningRate: float = 0.1

    reinforcementStrength: float = 1.25

    suppressionStrength: float = 0.75