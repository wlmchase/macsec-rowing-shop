import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';

const Cart = () => {
    const { cart, updateQuantity, removeFromCart, clearCart } = useCart();
    const navigate = useNavigate();

    const calculateTotal = () => {
        return cart.reduce((total, item) => total + item.price * item.quantity, 0);
    };

    const handleCheckout = () => {
        navigate('/checkout');
    };

    const handleQuantityChange = (itemId, newQuantity) => {
        const item = cart.find(i => i.id === itemId);
        if (!item) return;

        // Don't allow quantity to exceed available stock
        if (newQuantity > item.stock) {
            return;
        }

        // Don't allow quantity to be less than 1
        if (newQuantity < 1) {
            return;
        }

        updateQuantity(itemId, newQuantity);
    };

    if (cart.length === 0) {
        return (
            <div className="max-w-2xl mx-auto p-4">
                <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>
                <div className="bg-white shadow rounded-lg p-6 text-center">
                    <p className="text-gray-500">Your cart is empty</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-2xl mx-auto p-4">
            <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>
            
            <div className="bg-white shadow rounded-lg overflow-hidden">
                <ul className="divide-y divide-gray-200">
                    {cart.map((item) => (
                        <li key={item.id} className="p-4">
                            <div className="flex justify-between items-center">
                                <div className="flex-1">
                                    <h3 className="text-lg font-medium text-gray-900">{item.name}</h3>
                                    <p className="text-gray-500">${item.price.toFixed(2)}</p>
                                    <p className="text-sm text-gray-500">Available stock: {item.stock}</p>
                                </div>
                                <div className="flex items-center space-x-4">
                                    <div className="flex items-center space-x-2">
                                        <button
                                            onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                                            className="text-gray-500 hover:text-gray-700"
                                            disabled={item.quantity <= 1}
                                        >
                                            -
                                        </button>
                                        <span className="text-gray-700">{item.quantity}</span>
                                        <button
                                            onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                                            className="text-gray-500 hover:text-gray-700"
                                            disabled={item.quantity >= item.stock}
                                        >
                                            +
                                        </button>
                                    </div>
                                    <button
                                        onClick={() => removeFromCart(item.id)}
                                        className="text-red-500 hover:text-red-700"
                                    >
                                        Remove
                                    </button>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>

                <div className="p-4 border-t border-gray-200">
                    <div className="flex justify-between items-center mb-4">
                        <span className="text-lg font-medium">Total:</span>
                        <span className="text-xl font-bold">${calculateTotal().toFixed(2)}</span>
                    </div>
                    <div className="flex space-x-4">
                        <button
                            onClick={handleCheckout}
                            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                        >
                            Proceed to Checkout
                        </button>
                        <button
                            onClick={clearCart}
                            className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300"
                        >
                            Clear Cart
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Cart;