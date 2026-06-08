from pydantic import BaseModel


class DistributionRequest(BaseModel):

    filePath: str

    selectedColumn: str

    sampleSize: int = 100000