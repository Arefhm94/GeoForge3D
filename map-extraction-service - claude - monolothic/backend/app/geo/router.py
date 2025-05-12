from fastapi import APIRouter, HTTPException
from typing import List
from .models import Rectangle, GeoJSON
from ..extract import extract_building_footprints

router = APIRouter()

@router.post("/extract", response_model=GeoJSON)
async def extract_geojson(rectangle: Rectangle):
    if rectangle.area > 1000000:  # area in square meters
        raise HTTPException(status_code=400, detail="Area exceeds free limit of 1 km².")
    
    geojson_data = await extract_building_footprints(rectangle)
    return geojson_data

@router.get("/layers", response_model=List[str])
async def get_layers():
    # This should return available layers for the map
    return ["Buildings", "Parks", "Water Bodies", "Roads"]  # Example layers

@router.post("/rectangle", response_model=Rectangle)
async def create_rectangle(rectangle: Rectangle):
    # Logic to save the rectangle if needed
    return rectangle