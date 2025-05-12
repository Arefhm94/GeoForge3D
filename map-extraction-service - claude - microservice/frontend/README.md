# Frontend Documentation

This project is a web application that allows users to interact with a world map, search for locations, draw rectangles, and extract geographical data. The frontend is built using React and communicates with a backend powered by FastAPI.

## Features

- **World Map Display**: Users can view a world map with various layers.
- **Search Functionality**: A search bar allows users to find specific locations on the map.
- **Layer Selector**: Users can choose different layers to display on the map.
- **Drawing Tools**: Users can draw rectangles on the map to specify areas of interest.
- **GeoJSON Export**: Users can export the drawn rectangles as GeoJSON files.
- **Building Footprint Extraction**: The application can extract building footprints within the specified rectangles.
- **User Authentication**: Users can create accounts, log in, and manage their profiles.
- **Payment Integration**: Users can pay for data extraction beyond the free limit.

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Access to the backend services (user-service, map-service, payment-service).

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd map-extraction-service/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

### Running the Application

To start the development server, run:
```
npm start
```
The application will be available at `http://localhost:3000`.

### Folder Structure

- `public/`: Contains static files like `index.html` and `favicon.ico`.
- `src/`: Contains the React components, services, hooks, and styles.
  - `components/`: Contains all the React components organized by functionality.
  - `services/`: Contains API service files for interacting with the backend.
  - `hooks/`: Contains custom hooks for managing state and functionality.
  - `App.jsx`: The main application component.
  - `index.jsx`: The entry point for the React application.
  - `styles.css`: Contains the CSS styles for the application.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.