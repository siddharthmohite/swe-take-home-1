from datetime import datetime
from fastapi import HTTPException
import pandas as pd
from scipy.stats import linregress
from db.queries import fetch_trends_data, fetch_date_range

def analyze_trend(dates: pd.Series, values: pd.Series, unit: str) -> dict:

    if len(dates) < 2:
        return {"direction": "stable", "rate": 0.0, "unit": f"{unit}/month", "confidence": 0.0}
    
    slope, intercept, r_value, p_value, std_err = linregress(dates, values)
    direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
    rate = slope * 30  # Convert daily rate to monthly
    confidence = r_value ** 2  # R-squared
    
    return {
        "direction": direction,
        "rate": rate,
        "unit": f"{unit}/month",
        "confidence": confidence
    }

def detect_anomalies(df: pd.DataFrame) -> list:

    if df.empty:
        return []
    
    Q1 = df["value"].quantile(0.25)
    Q3 = df["value"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = df[
        (df["value"] < lower_bound) | (df["value"] > upper_bound)
    ].apply(lambda x: {
        "date": x["date"],
        "value": x["value"],
        "deviation": max(abs(x["value"] - lower_bound), abs(x["value"] - upper_bound)),
        "quality": x["quality"]
    }, axis=1).tolist()
    
    return anomalies

def analyze_seasonality(df: pd.DataFrame) -> dict:

    if df.empty:
        return {"detected": False, "period": None, "confidence": 0.0, "pattern": {}}
    
    df["month"] = pd.to_datetime(df["date"]).dt.month
    seasonal_avg = df.groupby("month")["value"].mean().to_dict()
    detected = len(seasonal_avg) > 1
    period = "yearly" if detected else None
    seasonality_confidence = 0.5 if detected else 0.0  # Arbitrary, improve with time-series
    
    season_map = {
        12: "winter", 1: "winter", 2: "winter",
        3: "spring", 4: "spring", 5: "spring",
        6: "summer", 7: "summer", 8: "summer",
        9: "fall", 10: "fall", 11: "fall"
    }
    seasonal_pattern = {}
    for month, avg in seasonal_avg.items():
        season = season_map.get(month, "unknown")
        seasonal_pattern[season] = {"avg": avg, "trend": "stable"}  # Simplified trend
    
    return {
        "detected": detected,
        "period": period,
        "confidence": seasonality_confidence,
        "pattern": seasonal_pattern
    }

def get_trends_processor(location_id, 
              start_date, 
              end_date, 
              metric, 
              quality_threshold):
 
    QUALITY_ORDER = ["poor", "questionable", "good", "excellent"]
    
    if not start_date or not end_date:
        default_start_date, default_end_date = fetch_date_range(
            location_id=location_id,
            metric=metric,
            quality_threshold=quality_threshold,
            valid_qualities=QUALITY_ORDER[QUALITY_ORDER.index(quality_threshold):] if quality_threshold else None
        )
        start_date = start_date or default_start_date
        end_date = end_date or default_end_date

    if quality_threshold and quality_threshold not in QUALITY_ORDER:
        raise HTTPException(status_code=400, detail="Invalid quality_threshold. Must be one of: poor, questionable, good, excellent")
    
    valid_qualities = QUALITY_ORDER[QUALITY_ORDER.index(quality_threshold):] if quality_threshold else None

    data = fetch_trends_data(
        location_id=location_id,
        start_date=start_date,
        end_date=end_date,
        metric=metric,
        quality_threshold=quality_threshold,
        valid_qualities=valid_qualities
    )

    if not data:
        raise HTTPException(status_code=400, message="No data available for the specified filters.")
    
    grouped_data = {}
    for row in data:
        metric_name = row["metric_name"]
        if metric_name not in grouped_data:
            grouped_data[metric_name] = {
                "metric_name": metric_name,
                "metric_unit": row["metric_unit"],
                "data_points": []
            }
        grouped_data[metric_name]["data_points"].append({
            "date": row["date"],
            "value": row["value"],
            "quality": row["quality"]
        })

    processed_data = list(grouped_data.values())

    for row in processed_data:
        df = pd.DataFrame(row["data_points"])
        if len(df) < 5:
            raise HTTPException(status_code=400, detail=f"Insufficient data for {row['metric_name']}: At least 5 data points are required for trend analysis.")
        
    result = {"data": {}}
    for row in processed_data:
        metric_name = row["metric_name"]
        unit = row["metric_unit"]

        df = pd.DataFrame(row["data_points"])
        if df.empty:
            continue

        trend = analyze_trend(
            dates=(pd.to_datetime(df["date"]) - pd.to_datetime(start_date)).dt.days,
            values=df["value"],
            unit=unit
        )
        anomalies = detect_anomalies(df)
        seasonality = analyze_seasonality(df)

        result["data"][metric_name] = {
            "trend": trend,
            "anomalies": anomalies,
            "seasonality": seasonality
        }

    return result