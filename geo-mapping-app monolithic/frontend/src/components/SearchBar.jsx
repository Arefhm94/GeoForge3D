import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSearch = (event) => {
        event.preventDefault();
        if (query) {
            onSearch(query);
            setQuery('');
        }
    };

    return (
        <form onSubmit={handleSearch} style={{ display: 'flex', margin: '20px' }}>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for a location"
                style={{ flex: 1, padding: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
            />
            <button type="submit" style={{ padding: '10px', marginLeft: '10px', borderRadius: '4px', backgroundColor: '#007bff', color: 'white' }}>
                Search
            </button>
        </form>
    );
};

export default SearchBar;