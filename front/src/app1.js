import React, { useState } from 'react';
import Footer from './components/Footer';
import Header from './components/Header';
import { Routes, Route, BrowserRouter as Router, Navigate } from 'react-router-dom';
import Signup from './modules/Signup';
import Home from './modules/Home';
import Scraper from './modules/Scraper';
import LinkList from './components/LinkList';
import { AuthProvider, useAuth } from './contexts/AuthContext';

function App() {
  const { isAuthenticated, login, logout } = useAuth();

  return (
    <AuthProvider>
      <Router>
        <div>
          <Header isAuthenticated={isAuthenticated} onLogout={logout} />
          <Routes>
            <Route
              path="/"
              element={<Home isAuthenticated={isAuthenticated} onLogin={login} />}
            />
            <Route path="/signup" element={<Signup />} />
            {isAuthenticated ? (
              <>
                <Route path="/scraper" element={<Scraper />} />
                <Route path="/linklist" element={<LinkList />} />
              </>
            ) : (
              <Navigate to="/" />
            )}
            <Route path="*" element={<div>404</div>} />
          </Routes>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
