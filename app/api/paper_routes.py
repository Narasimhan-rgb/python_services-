from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.paper_analysis import analyze_csv

router = APIRouter(prefix='/paper', tags=['Measured JMH results'])

@router.post('/analyze')
async def analyze(file: UploadFile = File(...)):
    raw = await file.read(10 * 1024 * 1024 + 1)
    await file.close()
    try:
        return analyze_csv(raw)
    except (ValueError, UnicodeError, KeyError, TypeError) as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
