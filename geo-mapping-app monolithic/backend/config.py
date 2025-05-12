import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FREE_DATA_LIMIT = 1000000  # 1 km² in square meters
    EXTRA_DATA_COST_PER_SQ_M = 2  # $2 per square meter
    GEOJSON_EXPORT_PATH = os.environ.get('GEOJSON_EXPORT_PATH') or '/path/to/export'