from fastapi import APIRouter, HTTPException

from app.models.distribution_request import DistributionRequest
from app.models.distribution_response import DistributionResponse
from app.services.distribution_detector import DistributionDetector


router = APIRouter(
    prefix="/detect",
    tags=["Distribution Detection"]
)

detector = DistributionDetector()


@router.post(
    "/distribution",
    response_model=DistributionResponse
)
def detect_distribution(
        request: DistributionRequest
):

    try:

        result = detector.detect_distribution(
            file_path=request.filePath,
            selected_column=request.selectedColumn,
            sample_size=request.sampleSize
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )