# Geo Extract Application Backend

## Overview
The Geo Extract Application is a web application that allows users to interact with a world map, create rectangular selections, and extract building footprints in GeoJSON format. The application includes user account management, a pricing model for data extraction, and a robust backend built with FastAPI.

## Features
- **World Map Display**: Users can view and interact with a world map.
- **Search Bar**: A search functionality to find locations on the map.
- **Layer Selector**: Users can select different layers to display on the map.
- **Rectangle Creation**: Users can draw rectangles on the map to specify areas for data extraction.
- **GeoJSON Export**: The application allows users to export the selected rectangle as a GeoJSON file.
- **Building Footprint Extraction**: Users can extract building footprints for the selected area.
- **User Account Management**: Users can create accounts, log in, and manage their profiles.
- **Pricing Model**: The first 1 km² of data extraction is free, with a fee of $2 per square meter thereafter.
- **Database Management**: A database system is implemented to manage user information, orders, and downloads.

## Technology Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React
- **Database**: PostgreSQL (or any preferred database)
- **Containerization**: Docker

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd geo-extract-app/backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Run the SQL commands in `database/schema.sql` to initialize the database schema.

4. Start the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints
- **Authentication**:
  - `POST /auth/register`: Register a new user.
  - `POST /auth/login`: Log in an existing user.
  - `GET /auth/profile`: Get user profile information.

- **Geo Extraction**:
  - `POST /geo/extract`: Extract building footprints for a specified rectangle.
  - `GET /geo/export`: Export the selected rectangle as GeoJSON.

- **Orders**:
  - `POST /orders/create`: Create a new order for data extraction.
  - `GET /orders/history`: Retrieve the user's order history.

## Testing
To run the tests, navigate to the `tests` directory and execute:
```
pytest
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.