# Geo Building Extractor

## Overview
The Geo Building Extractor is a web application that allows users to interact with a world map, draw rectangles to extract building footprints, and manage user accounts for data extraction services. The application is built using a microservice architecture with a Python backend and a React frontend.

## Features
- **World Map Display**: Users can view a world map with various layers.
- **Search Functionality**: A search bar allows users to find specific locations on the map.
- **Rectangle Drawing Tool**: Users can create rectangles on the map to specify areas for data extraction.
- **GeoJSON Export**: Users can export the drawn rectangle as a GeoJSON file.
- **Building Footprint Extraction**: The application extracts building footprints within the specified rectangle.
- **User Account Management**: Users can create accounts, log in, and manage their profiles.
- **Payment Integration**: The first 1 km² of data extraction is free, with a fee of $2 per additional square meter.
- **Microservice Architecture**: The application is structured into multiple services for scalability and maintainability.

## Project Structure
```
geo-building-extractor
├── frontend                # React frontend application
│   ├── public             # Public assets
│   ├── src                # Source code for the frontend
│   └── package.json       # Frontend dependencies and scripts
├── backend                 # Python backend services
│   ├── gateway-service     # Gateway service for routing
│   ├── auth-service        # User authentication service
│   ├── map-service         # Map-related functionalities
│   ├── extraction-service   # Building footprint extraction service
│   └── payment-service      # Payment processing service
├── database                # Database schema and migrations
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## Getting Started
1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd geo-building-extractor
   ```

2. **Set Up Environment Variables**: 
   Copy `.env.example` to `.env` and fill in the required values.

3. **Run the Application**: 
   Use Docker Compose to start the application:
   ```
   docker-compose up
   ```

4. **Access the Application**: 
   Open your browser and navigate to `http://localhost:3000` to view the application.

## License
This project is licensed under the MIT License. See the LICENSE file for details.