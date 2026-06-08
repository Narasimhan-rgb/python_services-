from pydantic import BaseModel


class ProfilingRequest(BaseModel):

    filePath: str

    selectedColumn: str

    sampleSize: int = 100000