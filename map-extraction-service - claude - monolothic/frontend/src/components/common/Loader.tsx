import React from 'react';

const Loader: React.FC = () => {
    return (
        <div className="loader">
            <div className="spinner"></div>
            <style jsx>{`
                .loader {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .spinner {
                    border: 8px solid rgba(255, 255, 255, 0.3);
                    border-top: 8px solid #ffffff;
                    border-radius: 50%;
                    width: 60px;
                    height: 60px;
                    animation: spin 1s linear infinite;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
};

export default Loader;