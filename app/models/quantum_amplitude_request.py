from pydantic import BaseModel


class QuantumAmplitudeRequest(BaseModel):

    filePath: str

    selectedColumn: str

    sampleSize: int = 100000

    candidateCount: int = 10

    learningRate: float = 0.1