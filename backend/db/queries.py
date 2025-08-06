from sqlalchemy import case, func, select, and_
from typing import  List, Optional
from .models import ClimateData, Location, Metric
from db.execute import execute_query as execute_query

PER_PAGE = 50

QUALITY_LEVELS = ["poor", "questionable", "good", "excellent"]

def _quality_thresholds_from(min_quality: str) -> list[str]:
    if min_quality not in QUALITY_LEVELS:
        return QUALITY_LEVELS
    index = QUALITY_LEVELS.index(min_quality)
    return QUALITY_LEVELS[index:]  # Return current and better levels

def fetch_climate_data(
    location_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = None,
    quality_threshold: Optional[str] = None,
    page: int = 1
):
    # Step 1: Build conditions
    filters = []

    if location_id:
        filters.append(ClimateData.location_id == location_id)
    if start_date:
        filters.append(ClimateData.date >= start_date)
    if end_date:
        filters.append(ClimateData.date <= end_date)
    if metric:
        filters.append(Metric.name == metric)
    if quality_threshold:
        filters.append(ClimateData.quality.in_(_quality_thresholds_from(quality_threshold)))

    # Step 2: Build query
    stmt = (
        select(
            ClimateData.id.label("climate_id"),
            ClimateData.date,
            ClimateData.value,
            ClimateData.quality,
            Location.id.label("location_id"),
            Location.name.label("location_name"),
            Location.latitude,
            Location.longitude,
            Metric.id.label("metric_id"),
            Metric.name.label("metric_name"),
            Metric.unit.label("metric_unit")
        )
        .select_from(ClimateData)
        .join(Location, ClimateData.location_id == Location.id)
        .join(Metric, ClimateData.metric_id == Metric.id)
        .where(and_(*filters))
        .limit(PER_PAGE)
        .offset((page - 1) * PER_PAGE)
    )
    # stmt = select(ClimateData, Location)
    # Step 3: Execute query
    results = execute_query(stmt ,as_mappings=True)

    return results


def get_all_locations():
   
   stmt = select(
        Location.id.label("location_id"),
        Location.name.label("location_name"),
        Location.country.label("country_name"),
        Location.latitude.label("latitude"),
        Location.longitude.label("longitude")
    )
   results = execute_query(stmt, as_mappings=True)

   return results

def get_all_metrics():
   
   stmt = select(
        Metric.id.label("metric_id"),
        Metric.name.label("metric_name"),
        Metric.display_name.label("display_name"),
        Metric.unit.label("unit"),
        Metric.description.label("description")
    )
   results = execute_query(stmt, as_mappings=True)
   
   return results

def fetch_summary_data(
    location_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    metric: Optional[str] = None,
    quality_threshold: Optional[str] = None,
    valid_qualities: Optional[List[str]] = None
) -> List[dict]:
   
    # Build conditions
    filters = []
    if location_id:
        filters.append(ClimateData.location_id == location_id)
    if start_date:
        filters.append(ClimateData.date >= start_date)
    if end_date:
        filters.append(ClimateData.date <= end_date)
    if metric:
        filters.append(Metric.name == metric)
    if quality_threshold:
        filters.append(ClimateData.quality.in_(valid_qualities))

    # Define quality weights for weighted_avg
    quality_weights = {
        "excellent": 1.0,
        "good": 0.8,
        "questionable": 0.5,
        "poor": 0.2
    }

    # Build query with aggregations
    stmt = (
        select(
            Metric.name.label("metric_name"),
            Metric.unit.label("metric_unit"),
            func.min(ClimateData.value).label("min_value"),
            func.max(ClimateData.value).label("max_value"),
            func.avg(ClimateData.value).label("avg_value"),
            func.sum(
                ClimateData.value * case(
                    {q: w for q, w in quality_weights.items()},
                    value=ClimateData.quality,
                    else_=0.0
                )
            ).label("weighted_sum"),
            func.sum(
                case(
                    {q: w for q, w in quality_weights.items()},
                    value=ClimateData.quality,
                    else_=0.0
                )
            ).label("weight_sum"),
            func.sum(case({ "excellent": 1 }, value=ClimateData.quality, else_=0)).label("excellent_count"),
            func.sum(case({ "good": 1 }, value=ClimateData.quality, else_=0)).label("good_count"),
            func.sum(case({ "questionable": 1 }, value=ClimateData.quality, else_=0)).label("questionable_count"),
            func.sum(case({ "poor": 1 }, value=ClimateData.quality, else_=0)).label("poor_count"),
            func.count().label("total_count")
        )
        .select_from(ClimateData)
        .join(Metric, ClimateData.metric_id == Metric.id)
        .where(and_(*filters))
        .group_by(Metric.name, Metric.unit)
    )

    results = execute_query(stmt, as_mappings=True)

    return results