# World Map App

## Overview
The World Map App is a web application that allows users to interact with a world map. Users can search for locations, create rectangles on the map, and export GeoJSON data of those rectangles. The application also provides functionality to extract building footprints from the specified area.

## Features
- Interactive world map with search functionality
- Layer selector for different map views
- Rectangle creation on the map
- Export GeoJSON of created rectangles
- Extract building footprints from specified rectangles
- User account creation and management
- Free access to the first 1 km² of data extracted, with a fee of $2 per square meter thereafter

## Tech Stack
- **Frontend**: React
- **Backend**: FastAPI (Python)
- **Database**: SQL (managed through migrations)
- **Containerization**: Docker

## Project Structure
```
world-map-app
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── api
│   │   │   ├── auth.py
│   │   │   ├── map.py
│   │   │   └── billing.py
│   │   ├── models
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── geojson_exporter.py
│   │   │   ├── building_extractor.py
│   │   │   └── billing_calculator.py
│   │   └── database
│   │       └── db.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── components
│   │   │   ├── Map.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   └── LayerSelector.jsx
│   │   ├── pages
│   │   │   ├── Home.jsx
│   │   │   ├── Signup.jsx
│   │   │   └── Pricing.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── database
│   ├── migrations
│   └── schema.sql
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Backend
1. Navigate to the `backend` directory.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend
1. Navigate to the `frontend` directory.
2. Install the required dependencies:
   ```
   npm install
   ```
3. Start the React application:
   ```
   npm start
   ```

### Database
- Ensure that the database is set up according to the schema defined in `database/schema.sql`.
- Run migrations as necessary to keep the database schema up to date.

## Usage
- Users can sign up for an account through the Signup page.
- After logging in, users can access the map, search for locations, create rectangles, and manage their data extraction requests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.