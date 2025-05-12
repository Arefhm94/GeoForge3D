from flask import Flask
from flask_cors import CORS
from api.auth import auth_bp
from api.map_data import map_data_bp
from api.buildings import buildings_bp
from api.payments import payments_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(map_data_bp, url_prefix='/api/map')
app.register_blueprint(buildings_bp, url_prefix='/api/buildings')
app.register_blueprint(payments_bp, url_prefix='/api/payments')

if __name__ == '__main__':
    app.run(debug=True)