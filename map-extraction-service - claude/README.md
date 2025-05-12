# Map Extraction Service

This project is a web application designed to provide users with the ability to interact with a world map, search for locations, draw rectangles, and extract geographical data in GeoJSON format. The application is built using a microservices architecture, with a frontend developed in React and backend services implemented in Python using FastAPI.

## Features

- **World Map Display**: Users can view a world map with various layers.
- **Search Functionality**: A search bar allows users to find specific locations on the map.
- **Layer Selector**: Users can choose different layers to display on the map.
- **Rectangle Drawing**: Users can draw rectangles on the map to specify areas of interest.
- **GeoJSON Export**: The application can export the drawn rectangles as GeoJSON files.
- **Building Footprint Extraction**: Users can extract building footprints within the specified rectangles.
- **User Authentication**: Users can create accounts, log in, and manage their profiles.
- **Payment Processing**: The first 1 km² of data extraction is free, with a fee of $2 per square meter thereafter.
- **Database Management**: User information and order details are managed in a database.

## Architecture

The application is structured into several microservices:

- **User Service**: Handles user authentication and management.
- **Map Service**: Manages map-related functionalities, including drawing and GeoJSON export.
- **Payment Service**: Processes payments for data extraction.
- **API Gateway**: Routes requests to the appropriate services.

## Getting Started

To run the application locally, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd map-extraction-service
   ```

2. Set up the database:
   - Run the SQL commands in `database/schema.sql` to create the necessary tables.

3. Build and run the services using Docker Compose:
   ```
   docker-compose up --build
   ```

4. Access the frontend application at `http://localhost:3000`.

## Technologies Used

- **Frontend**: React
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (or any other preferred database)
- **Docker**: For containerization
- **Nginx**: For serving the application and handling requests

## License

This project is licensed under the MIT License. See the LICENSE file for more details.