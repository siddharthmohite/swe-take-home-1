from fastapi import APIRouter
from processors.locations import get_locations_processor as get_locations_processor
router = APIRouter()

@router.get("/")
def get_locations():
    
    return get_locations_processor()
