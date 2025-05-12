import React, { useState } from 'react';

const DrawTools = ({ onRectangleDraw }) => {
    const [drawing, setDrawing] = useState(false);
    const [startPoint, setStartPoint] = useState(null);
    const [endPoint, setEndPoint] = useState(null);

    const handleMouseDown = (e) => {
        setDrawing(true);
        setStartPoint({ x: e.clientX, y: e.clientY });
    };

    const handleMouseMove = (e) => {
        if (!drawing) return;
        setEndPoint({ x: e.clientX, y: e.clientY });
    };

    const handleMouseUp = () => {
        if (drawing && startPoint && endPoint) {
            const rectangle = {
                start: startPoint,
                end: endPoint,
            };
            onRectangleDraw(rectangle);
        }
        setDrawing(false);
        setStartPoint(null);
        setEndPoint(null);
    };

    return (
        <div
            className="draw-tools"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            style={{ position: 'relative', width: '100%', height: '100%' }}
        >
            {drawing && startPoint && endPoint && (
                <div
                    style={{
                        position: 'absolute',
                        left: Math.min(startPoint.x, endPoint.x),
                        top: Math.min(startPoint.y, endPoint.y),
                        width: Math.abs(startPoint.x - endPoint.x),
                        height: Math.abs(startPoint.y - endPoint.y),
                        border: '2px dashed red',
                        pointerEvents: 'none',
                    }}
                />
            )}
        </div>
    );
};

export default DrawTools;