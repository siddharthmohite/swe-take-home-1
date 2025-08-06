from fastapi import APIRouter
from typing import Optional
from db.queries import fetch_climate_data as fetch_climate_data
router = APIRouter()

@router.get("/")
def get_climate(
                      location_id: Optional[int] = None, 
                      start_date: Optional[str] = None, 
                      end_date: Optional[str] = None, 
                      metric: Optional[str] = None, 
                      quality_threshold: Optional[float] = None):
    
    results = fetch_climate_data(location_id=location_id, 
                                      start_date=start_date, 
                                      end_date=end_date, 
                                      metric=metric, 
                                      quality_threshold=quality_threshold)
    
    data = []

    for record in results:
        data.append({
            "id": record.get("climate_id", "NA"),
            "location_id": record.get("location_id", "NA"),
            "location_name": record.get("location_name", "NA"),
            "latitude": record.get("latitude", "NA"),
            "longitude": record.get("longitude", "NA"),
            "date": record.get("date", "NA"),
            "metric": record.get("metric_name", "NA"),
            "value": record.get("value", "NA"),
            "unit": record.get("metric_unit", "NA"),
            "quality": record.get("quality", "NA"),
        })
    
    total_count = len(data)
    response = {
        "data": data,
        "meta": {
            "total_count": total_count,
            "page": 1,
            "per_page": total_count 
        }
    } 
        
    return response
