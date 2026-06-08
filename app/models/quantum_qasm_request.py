from pydantic import BaseModel


class QuantumQasmRequest(BaseModel):

    filePath: str

    selectedColumn: str

    sampleSize: int = 100000

    candidateCount: int = 5

    learningRate: float = 0.1