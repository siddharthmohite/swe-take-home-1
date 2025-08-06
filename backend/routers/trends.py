from fastapi import APIRouter, HTTPException
from typing import Optional
from processors.trends import get_trends_processor as get_trends_processor

router = APIRouter()

@router.get("/")
def get_trends(
    location_id: Optional[int] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None, 
    metric: Optional[str] = None, 
    quality_threshold: Optional[str] = None
):

    return get_trends_processor(location_id, start_date, end_date, metric, quality_threshold)