import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/residencia-fiscal-paraguay" element={<LandingPage />} />
        {/* Redirección por defecto para facilitar la navegación durante el desarrollo/test */}
        <Route path="/" element={<Navigate to="/residencia-fiscal-paraguay" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
