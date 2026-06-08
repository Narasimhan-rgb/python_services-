from fastapi import APIRouter, HTTPException

from app.models.profiling_request import ProfilingRequest
from app.models.profiling_response import ProfilingResponse
from app.services.polars_dataset_profiler import PolarsDatasetProfiler


router = APIRouter(
    prefix="/profile",
    tags=["Dataset Profiling"]
)

profiler = PolarsDatasetProfiler()


@router.post(
    "/dataset",
    response_model=ProfilingResponse
)
def profile_dataset(
        request: ProfilingRequest
):

    try:

        result = profiler.profile_dataset(
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