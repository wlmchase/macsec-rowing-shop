import React, { createContext, useContext, useState } from 'react';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
    const [cart, setCart] = useState([]);

    const addToCart = (product) => {
        console.log('Adding to cart:', product);
        setCart(currentCart => {
            const existingItem = currentCart.find(item => item.id === product.id);
            if (existingItem) {
                return currentCart.map(item =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            }
            return [...currentCart, { ...product, quantity: 1 }];
        });
    };

    const updateQuantity = (productId, newQuantity) => {
        console.log('Updating quantity:', productId, newQuantity);
        setCart(currentCart => {
            if (newQuantity === 0) {
                return currentCart.filter(item => item.id !== productId);
            }
            return currentCart.map(item =>
                item.id === productId
                    ? { ...item, quantity: newQuantity }
                    : item
            );
        });
    };

    const removeFromCart = (productId) => {
        console.log('Removing from cart:', productId);
        setCart(currentCart => currentCart.filter(item => item.id !== productId));
    };

    const clearCart = () => {
        console.log('Clearing cart');
        setCart([]);
    };

    const getCartTotal = () => {
        return cart.reduce((total, item) => total + item.price * item.quantity, 0);
    };

    const getCartItemCount = () => {
        return cart.reduce((total, item) => total + item.quantity, 0);
    };

    const value = {
        cart,
        addToCart,
        updateQuantity,
        removeFromCart,
        clearCart,
        getCartTotal,
        getCartItemCount,
    };

    return (
        <CartContext.Provider value={value}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
}; 