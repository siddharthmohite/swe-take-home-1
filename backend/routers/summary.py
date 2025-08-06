from fastapi import APIRouter, HTTPException
from typing import Optional
from processors.summary import get_summary_processor as get_summary_processor

router = APIRouter()

@router.get("/")
def get_summary(
    location_id: Optional[int] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    metric: Optional[str] = None, 
    quality_threshold: Optional[str] = None
):

    return get_summary_processor(location_id, start_date, end_date, metric, quality_threshold)