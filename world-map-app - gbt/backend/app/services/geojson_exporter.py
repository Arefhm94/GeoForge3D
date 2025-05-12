from fastapi import HTTPException
import geojson

class GeoJSONExporter:
    def __init__(self, rectangle):
        self.rectangle = rectangle

    def export(self):
        if not self.rectangle or len(self.rectangle) != 4:
            raise HTTPException(status_code=400, detail="Invalid rectangle data")

        geojson_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [self.rectangle[0], self.rectangle[1]],
                    [self.rectangle[2], self.rectangle[1]],
                    [self.rectangle[2], self.rectangle[3]],
                    [self.rectangle[0], self.rectangle[3]],
                    [self.rectangle[0], self.rectangle[1]]
                ]]
            },
            "properties": {}
        }

        return geojson.dumps(geojson_feature)