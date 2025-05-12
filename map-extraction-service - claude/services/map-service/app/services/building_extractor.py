from typing import List, Dict
import requests

class BuildingExtractor:
    def __init__(self, map_service_url: str):
        self.map_service_url = map_service_url

    def extract_building_footprints(self, rectangle: Dict[str, float]) -> List[Dict]:
        response = requests.post(f"{self.map_service_url}/extract-buildings", json=rectangle)
        if response.status_code == 200:
            return response.json().get("buildings", [])
        else:
            response.raise_for_status()

    def rectangle_to_geojson(self, rectangle: Dict[str, float]) -> Dict:
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [rectangle["west"], rectangle["south"]],
                            [rectangle["east"], rectangle["south"]],
                            [rectangle["east"], rectangle["north"]],
                            [rectangle["west"], rectangle["north"]],
                            [rectangle["west"], rectangle["south"]],
                        ]]
                    },
                    "properties": {}
                }
            ]
        }
        return geojson