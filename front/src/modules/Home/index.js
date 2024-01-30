import React from 'react';
import Login from '../Login';
import YouTube from 'react-youtube';

const Home = ({ isAuthenticated, onLogin }) => {
  const videoId = '0fYi8SGA20k'; // Replace with the actual YouTube video ID

  const opts = {
    height: '360', // Set the height of the video frame
    width: '640',  // Set the width of the video frame
  };

  return (
    <div>
      {isAuthenticated ? (
        // Render authenticated user's UI
        <div>
          {/* ... (authenticated user's content) */}
        </div>
      ) : (
        // Render non-authenticated user's UI
        <div>
          {<div className="flex">
      
      <Login isAuthenticated={isAuthenticated} onLogin={onLogin}/>
      <div>
        <YouTube videoId={videoId} opts={opts} />
      </div>
    </div>}
        </div>
      )}
    
    </div>
  );
};

export default Home;
