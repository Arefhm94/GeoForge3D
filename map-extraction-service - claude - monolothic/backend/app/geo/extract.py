from fastapi import APIRouter, HTTPException
from typing import List, Dict
import geojson
from .models import Rectangle, BuildingFootprint
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/extract/geojson", response_model=Dict)
def export_geojson(rectangle: Rectangle, db: Session = Depends(get_db)):
    # Logic to create GeoJSON from the rectangle
    geojson_data = geojson.FeatureCollection([])  # Placeholder for GeoJSON data
    return geojson_data

@router.post("/extract/building-footprints", response_model=List[BuildingFootprint])
def extract_building_footprints(rectangle: Rectangle, db: Session = Depends(get_db)):
    # Logic to extract building footprints within the rectangle
    footprints = []  # Placeholder for building footprints
    return footprints

@router.get("/extract/pricing/{area}", response_model=Dict)
def calculate_pricing(area: float):
    if area <= 1.0:
        return {"price": 0.0}  # First 1 km² is free
    else:
        price_per_square_meter = 2.0
        total_price = (area - 1.0) * price_per_square_meter
        return {"price": total_price}