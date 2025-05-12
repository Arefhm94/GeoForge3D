from flask import Flask
from flask_cors import CORS
from routes import main_routes
from middleware import error_handling

app = Flask(__name__)
CORS(app)

# Register routes
app.register_blueprint(main_routes)

# Apply middleware
app.before_request(error_handling)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)