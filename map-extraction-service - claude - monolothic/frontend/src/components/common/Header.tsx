import React from 'react';

const Header: React.FC = () => {
    return (
        <header>
            <h1>Geo Extract App</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/login">Login</a></li>
                    <li><a href="/register">Register</a></li>
                    <li><a href="/orders">Orders</a></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;