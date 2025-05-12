import React from 'react';
import './Button.css'; // Assuming you have a CSS file for button styles

const Button = ({ onClick, children, type = 'button', className = '' }) => {
    return (
        <button onClick={onClick} type={type} className={`custom-button ${className}`}>
            {children}
        </button>
    );
};

export default Button;