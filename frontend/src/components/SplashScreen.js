import React from 'react';
import './SplashScreen.css';

const SplashScreen = ({ onFinish }) => {
  React.useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 3000); // 3 seconds
    return () => clearTimeout(timer);
  }, [onFinish]);

  return (
    <div className="splash-screen">
      <div className="splash-content">
        <div className="splash-logo">
          <div className="splash-icon">🎁</div>
          <h2>CaseForge</h2>
        </div>
        <p className="splash-text">Opening virtual cases</p>
      </div>
    </div>
  );
};

export default SplashScreen;