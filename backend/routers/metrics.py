from fastapi import APIRouter
from db.queries import get_all_metrics as get_all_metrics
router = APIRouter()

@router.get("/")
async def get_locations():
    
    results = get_all_metrics()
    data = []
    for loc in results:
        data.append({
            "id": loc.get("metric_id", "NA"),
            "name": loc.get("metric_name", "NA"),
            "display_name": loc.get("display_name", "NA"),
            "unit": loc.get("unit", "NA"),
            "description": loc.get("description", "NA")
        })


    response = {
        "data":data
    }
    
    return response