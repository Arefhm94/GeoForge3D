# Geo Mapping App

## Overview
The Geo Mapping App is a web application that allows users to interact with a world map. Users can search for locations, select different map layers, draw rectangles on the map, and extract geographic data in GeoJSON format. The application also provides functionality for user authentication, payment processing, and managing user orders.

## Features
- **World Map Display**: Interactive map showing various geographic layers.
- **Search Bar**: Allows users to search for specific locations on the map.
- **Layer Selector**: Users can choose different layers to display on the map.
- **Rectangle Drawing**: Users can draw rectangles on the map to specify areas of interest.
- **GeoJSON Export**: Extract geographic data of the drawn rectangle in GeoJSON format.
- **Building Footprint Extraction**: Retrieve building footprints within the specified rectangle.
- **User Authentication**: Users can create accounts, log in, and manage their profiles.
- **Payment Processing**: First 1 km² of data extraction is free; subsequent extractions are charged at $2 per square meter.
- **Order Management**: Users can view their order history and download extracted data.

## Technology Stack
- **Frontend**: React
- **Backend**: Python (Flask)
- **Database**: SQL (defined in `schema.sql`)
- **Containerization**: Docker (defined in `docker-compose.yml`)

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd geo-mapping-app
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```

4. Run the application:
   - Start the backend server:
     ```
     python app.py
     ```
   - Start the frontend development server:
     ```
     npm start
     ```

## Usage
- Access the application in your web browser at `http://localhost:3000`.
- Create an account or log in to access the full features of the application.
- Use the search bar to find locations and interact with the map.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.