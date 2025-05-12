import React from 'react';
import Map from '../components/Map';
import SearchBar from '../components/SearchBar';
import LayerSelector from '../components/LayerSelector';

const Home = () => {
    return (
        <div>
            <h1>World Map Application</h1>
            <SearchBar />
            <LayerSelector />
            <Map />
        </div>
    );
};

export default Home;