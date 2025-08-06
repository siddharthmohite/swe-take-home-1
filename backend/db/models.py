from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class Location(Base):
    __tablename__ = "Locations"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    region = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    climate_data = relationship("ClimateData", back_populates="location")

class Metric(Base):
    __tablename__ = "Metrics"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    display_name = Column(String)
    unit = Column(String)
    description = Column(String)
    climate_data = relationship("ClimateData", back_populates="metric")

class ClimateData(Base):
    __tablename__ = "ClimateData"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("Locations.id"))
    metric_id = Column(Integer, ForeignKey("Metrics.id"))
    date = Column(Date)
    value = Column(Float)
    quality = Column(String)

    location = relationship("Location", back_populates="climate_data")
    metric = relationship("Metric", back_populates="climate_data")
