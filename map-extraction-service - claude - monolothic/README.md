# Geo Extract Application

## Overview
The Geo Extract Application is a web-based platform that allows users to interact with a world map, create rectangular selections, and extract building footprints in GeoJSON format. The application features user account management, a pricing model for data extraction, and a robust backend built with FastAPI and a frontend developed using React.

## Features
- **World Map Display**: Interactive map with search functionality and layer selection.
- **Rectangle Creation**: Users can draw rectangles on the map to specify areas for data extraction.
- **GeoJSON Export**: Extract building footprints as GeoJSON files based on user-defined rectangles.
- **User Accounts**: Users can create accounts, log in, and manage their profiles.
- **Pricing Model**: First 1 km² of data extraction is free; subsequent extractions are charged at $2 per square meter.
- **Database Management**: User information, orders, and downloads are managed through a database.

## Technology Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React (TypeScript)
- **Database**: SQL (PostgreSQL recommended)
- **Deployment**: Docker

## Project Structure
```
geo-extract-app
├── backend
│   ├── app
│   ├── tests
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend
│   ├── public
│   ├── src
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── database
│   ├── migrations
│   └── schema.sql
├── docker-compose.yml
└── README.md
```

## Getting Started
1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd geo-extract-app
   ```

2. **Backend Setup**:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the FastAPI application:
     ```
     uvicorn app.main:app --reload
     ```

3. **Frontend Setup**:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```
   - Start the React application:
     ```
     npm run dev
     ```

4. **Database Setup**:
   - Run the SQL commands in `database/schema.sql` to set up the initial database schema.
   - Apply migrations from `database/migrations/init.sql` as needed.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.