import React from 'react';
import './LoadingScreen.css';

const messages = [
  "Accessing classified archives...",
  "Cross-referencing disparate data streams...",
  "Synthesizing narrative threads...",
  "Extracting hidden entities...",
  "Please wait, the truth is being uncovered...",
  "Processing complete. Preparing insights...",
];

const LoadingScreen = () => {
  const [messageIndex, setMessageIndex] = React.useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
    }, 3000); // Change message every 3 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="loading-screen">
      <div className="loading-animation">
        {/* Placeholder for complex animation - could be SVG, CSS animation, or Lottie */}
        <div className="spinner"></div>
        <div className="scanner"></div>
      </div>
      <p className="loading-message">{messages[messageIndex]}</p>
      <div className="progress-bar-container">
        <div className="progress-bar"></div>
      </div>
    </div>
  );
};

export default LoadingScreen;
