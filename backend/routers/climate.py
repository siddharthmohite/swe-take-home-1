from fastapi import APIRouter
from typing import Optional
from db.queries import fetch_climate_data as fetch_climate_data
from processors.climate import get_climate_data as get_climate_data
router = APIRouter()

@router.get("/")
def get_climate(
                      location_id: Optional[int] = None, 
                      start_date: Optional[str] = None, 
                      end_date: Optional[str] = None, 
                      metric: Optional[str] = None, 
                      quality_threshold: Optional[str] = None):
    
    
    return get_climate_data(location_id, start_date, end_date, metric, quality_threshold)
