import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { CartProvider } from './contexts/CartContext';

// Import your components
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Products from './pages/Products';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import Profile from './pages/Profile';
import AdminDashboard from './pages/AdminDashboard';
import Contact from './pages/Contact';
import Layout from './components/Layout';
import OrderConfirmation from './pages/OrderConfirmation';

// Protected Route component
const ProtectedRoute = ({ children, requireAdmin = false }) => {
    const { isAuthenticated, isAdmin, loading } = useAuth();

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }

    if (requireAdmin && !isAdmin) {
        return <Navigate to="/" />;
    }

    return children;
};

function App() {
    return (
        <AuthProvider>
            <CartProvider>
                <Router>
                    <Layout>
                        <Routes>
                            {/* Public routes */}
                            <Route path="/" element={<Home />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/register" element={<Register />} />
                            <Route path="/products" element={<Products />} />
                            <Route path="/contact" element={<Contact />} />
                            
                            {/* Protected routes */}
                            <Route 
                                path="/cart" 
                                element={
                                    <ProtectedRoute>
                                        <Cart />
                                    </ProtectedRoute>
                                } 
                            />
                            <Route 
                                path="/checkout" 
                                element={
                                    <ProtectedRoute>
                                        <Checkout />
                                    </ProtectedRoute>
                                } 
                            />
                            <Route 
                                path="/profile" 
                                element={
                                    <ProtectedRoute>
                                        <Profile />
                                    </ProtectedRoute>
                                } 
                            />
                            
                            {/* Admin routes */}
                            <Route 
                                path="/admin" 
                                element={
                                    <ProtectedRoute requireAdmin>
                                        <AdminDashboard />
                                    </ProtectedRoute>
                                } 
                            />
                            
                            {/* Order Confirmation route */}
                            <Route 
                                path="/order-confirmation" 
                                element={
                                    <ProtectedRoute>
                                        <OrderConfirmation />
                                    </ProtectedRoute>
                                } 
                            />
                            
                            {/* Catch all route */}
                            <Route path="*" element={<Navigate to="/" />} />
                        </Routes>
                    </Layout>
                </Router>
            </CartProvider>
        </AuthProvider>
    );
}

export default App;