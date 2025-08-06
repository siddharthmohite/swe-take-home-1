from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.climate import router as climate_router
from routers.locations import router as locations_router
from routers.metrics import router as metrics_router
from routers.summary import router as summary_router
from routers.trends import router as trends_router


app = FastAPI(title="Climate API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(climate_router, prefix="/api/v1/climate", tags=["climate"])
app.include_router(locations_router, prefix="/api/v1/locations", tags=["locations"])
app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["metrics"])
app.include_router(summary_router, prefix="/api/v1/summary", tags=["summary"])
app.include_router(trends_router, prefix="/api/v1/trends", tags=["trends"])
