from fastapi import APIRouter
from processors.metrics import get_metrics_processor as get_metrics_processor
router = APIRouter()

@router.get("/")
def get_metrics():
    
    return get_metrics_processor()