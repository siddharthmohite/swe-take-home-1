from fastapi import HTTPException
from db.queries import fetch_summary_data as fetch_summary_data

def calculate_weighted_avg(weighted_sum: float, weight_sum: float) -> float:
    return weighted_sum / weight_sum if weight_sum > 0 else 0.0

def get_summary_processor(location_id, 
                start_date, 
                end_date, 
                metric, 
                quality_threshold):

    QUALITY_ORDER = ["poor", "questionable", "good", "excellent"]
    
    if quality_threshold and quality_threshold not in QUALITY_ORDER:
        raise HTTPException(status_code=400, detail="Invalid quality_threshold. Must be one of: poor, questionable, good, excellent")
    
    valid_qualities = QUALITY_ORDER[QUALITY_ORDER.index(quality_threshold):] if quality_threshold else None

    results = fetch_summary_data(
        location_id=location_id,
        start_date=start_date,
        end_date=end_date,
        metric=metric,
        quality_threshold=quality_threshold,
        valid_qualities=valid_qualities
    )

    result = {"data": {}}
    for row in results:
        metric_name = row["metric_name"]
        total_count = row["total_count"]
        if total_count == 0:
            continue

        quality_dist = {
            "excellent": row["excellent_count"] / total_count,
            "good": row["good_count"] / total_count,
            "questionable": row["questionable_count"] / total_count,
            "poor": row["poor_count"] / total_count
        }
        quality_dist_full = {q: quality_dist.get(q, 0.0) for q in QUALITY_ORDER}

        result["data"][metric_name] = {
            "min": row["min_value"],
            "max": row["max_value"],
            "avg": row["avg_value"],
            "weighted_avg": calculate_weighted_avg(row["weighted_sum"], row["weight_sum"]),
            "unit": row["metric_unit"],
            "quality_distribution": quality_dist_full
        }
    
    return result