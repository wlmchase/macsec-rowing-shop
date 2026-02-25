import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children, isAllowed = true }) => {
  const token = localStorage.getItem('token');

  if (!token || !isAllowed) {
    return <Navigate to="/login" />;
  }

  return children;
};

export default ProtectedRoute;