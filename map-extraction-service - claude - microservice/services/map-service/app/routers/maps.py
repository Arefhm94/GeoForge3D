from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class Rectangle(BaseModel):
    coordinates: List[float]  # [min_lat, min_lon, max_lat, max_lon]

class GeoJSONResponse(BaseModel):
    type: str
    features: List[Dict]

@router.post("/extract-geojson", response_model=GeoJSONResponse)
async def extract_geojson(rectangle: Rectangle):
    # Logic to extract GeoJSON data based on the rectangle coordinates
    # This is a placeholder for the actual implementation
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    return geojson_data

@router.get("/layers")
async def get_layers():
    # Logic to retrieve available map layers
    layers = ["Layer1", "Layer2", "Layer3"]  # Placeholder for actual layers
    return {"layers": layers}