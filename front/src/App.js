import React, { useState } from 'react';
import Footer from './components/Footer';
import Header from './components/Header';
import { Routes, Route } from 'react-router-dom';
import Signup from './modules/Signup';
import Home from './modules/Home';
import Scraper from './modules/Scraper';
import LinkList from './components/LinkList';
import Crons from './modules/Crons';
import YourCrons from './modules/YourCrons';
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  }

  const handleLogout = () => {
    setIsAuthenticated(false);
    // Perform any other logout tasks (e.g., clearing tokens or session data)
  }

  return (
    <div>
      <Header isAuthenticated={isAuthenticated} onLogout={handleLogout} />
      <div id="root">
        <Routes>
          <Route path="/" element={<Home isAuthenticated={isAuthenticated} onLogin={handleLogin} />} />
          {/* <Route path="/login" element={<Login/>} /> */}
          <Route path="/signup" element={<Signup />} />
          <Route path="/scraper" element={<Scraper />} />
          <Route path="/linklist" element={<LinkList />} />
          <Route path="/crons" element={<Crons />} />
          <Route path="/yourcrons" element={<YourCrons />} />
          <Route path="*" element={<div>404</div>} />
        </Routes>
      </div>
      <Footer />
    </div>
  );
}

export default App;
