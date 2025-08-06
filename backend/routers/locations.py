from fastapi import APIRouter
from db.queries import get_all_locations as get_all_locations
router = APIRouter()

@router.get("/")
async def get_locations():
    
    results = get_all_locations()
    data = []
    for loc in results:
        data.append({
            "id": loc.get("location_id", "NA"),
            "name": loc.get("location_name", "NA"),
            "name": loc.get("country_name", "NA"),
            "latitude": loc.get("latitude", "NA"),
            "longitude": loc.get("longitude", "NA")
        })


    response = {
        "data":data
    }

    return response
