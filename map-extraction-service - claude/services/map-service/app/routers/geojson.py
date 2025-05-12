from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json

router = APIRouter()

class Rectangle(BaseModel):
    coordinates: List[List[float]]

@router.post("/export-geojson", response_model=dict)
async def export_geojson(rectangle: Rectangle):
    try:
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [rectangle.coordinates]
                    },
                    "properties": {}
                }
            ]
        }
        return geojson
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/extract-buildings/{rectangle_id}", response_model=dict)
async def extract_buildings(rectangle_id: str):
    # Placeholder for building extraction logic
    # This should interact with the building_extractor service
    return {"message": "Building footprints extracted", "rectangle_id": rectangle_id}