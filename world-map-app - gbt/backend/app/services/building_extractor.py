from typing import List, Dict
import requests

class BuildingExtractor:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def extract_buildings(self, rectangle: Dict[str, float]) -> List[Dict]:
        response = requests.post(f"{self.api_url}/extract_buildings", json=rectangle)
        if response.status_code == 200:
            return response.json().get("buildings", [])
        else:
            response.raise_for_status()