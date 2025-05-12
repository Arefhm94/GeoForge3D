from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.geojson_exporter import export_geojson
from services.building_extractor import extract_building_footprints
from services.billing_calculator import calculate_billing

router = APIRouter()

class Rectangle(BaseModel):
    coordinates: List[List[float]]  # List of [longitude, latitude] pairs

@router.post("/create-rectangle")
async def create_rectangle(rectangle: Rectangle):
    # Logic to create a rectangle on the map
    geojson = export_geojson(rectangle.coordinates)
    return {"geojson": geojson}

@router.post("/extract-buildings")
async def extract_buildings(rectangle: Rectangle):
    # Logic to extract building footprints from the rectangle
    footprints = extract_building_footprints(rectangle.coordinates)
    return {"footprints": footprints}

@router.post("/calculate-billing")
async def calculate_billing_area(area: float):
    # Logic to calculate billing based on area
    amount = calculate_billing(area)
    return {"amount": amount}