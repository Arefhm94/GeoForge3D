# Geo Mapping App - Frontend

This is the frontend part of the Geo Mapping App, built using React. The application allows users to interact with a world map, search for locations, draw rectangles, and extract geographical data.

## Features

- **World Map Display**: Users can view a world map with various layers.
- **Search Bar**: A search functionality to find specific locations on the map.
- **Layer Selector**: Users can select different layers to visualize on the map.
- **Rectangle Drawing**: Users can draw rectangles on the map to specify areas of interest.
- **GeoJSON Export**: The ability to export the drawn rectangle as GeoJSON.
- **Building Footprint Extraction**: Extract building footprints within the specified rectangle.
- **User Authentication**: Users can create accounts, log in, and manage their profiles.
- **Payment Processing**: Users can pay for data extraction beyond the free limit.

## Getting Started

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/geo-mapping-app.git
   ```

2. **Navigate to the frontend directory**:
   ```
   cd geo-mapping-app/frontend
   ```

3. **Install dependencies**:
   ```
   npm install
   ```

4. **Run the application**:
   ```
   npm start
   ```

## Folder Structure

- `public/`: Contains the main HTML file and static assets.
- `src/`: Contains all React components, pages, and services.
  - `components/`: Reusable components like Map, SearchBar, LayerSelector, etc.
  - `pages/`: Different pages of the application like Dashboard, MapView, Profile, and Orders.
  - `services/`: API service files for handling requests to the backend.

## Dependencies

This project uses several npm packages. Check `package.json` for the complete list of dependencies.

## License

This project is licensed under the MIT License. See the LICENSE file for details.