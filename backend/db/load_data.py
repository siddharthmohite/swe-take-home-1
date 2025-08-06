import json
import os
from datetime import datetime

from models import Location, Metric, ClimateData
from session import engine, SessionLocal
from models import Base

from sqlalchemy.exc import IntegrityError

def load_data():
    # Load JSON
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_PATH = os.path.join(BASE_DIR, "data", "sample_data.json")
    with open(DATA_PATH, "r") as f:
        data = json.load(f)

    # Create tables
    Base.metadata.drop_all(bind=engine)  # Reset if needed
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        # Seed Locations
        for loc in data["locations"]:
            location = Location(
                id=loc["id"],
                name=loc["name"],
                country=loc["country"],
                region=loc.get("region", ""),
                latitude=loc["latitude"],
                longitude=loc["longitude"]
            )
            session.add(location)

        # Seed Metrics
        for met in data["metrics"]:
            metric = Metric(
                id=met["id"],
                name=met["name"],
                display_name=met["display_name"],
                unit=met["unit"],
                description=met["description"]
            )
            session.add(metric)

        session.commit()

        # Seed Climate Data
        for entry in data["climate_data"]:
            climate = ClimateData(
                location_id=entry["location_id"],
                metric_id=entry["metric_id"],
                date=datetime.strptime(entry["date"], "%Y-%m-%d").date(),
                value=entry["value"],
                quality=entry["quality"]
            )
            session.add(climate)

        session.commit()
        print("Loaded Data successfully.")
    except IntegrityError as e:
        print("Error Loading Data:", e)
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    load_data()
