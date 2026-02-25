import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import { orderAPI } from '../services/api.service';
import { useAuth } from '../contexts/AuthContext';
import { validateShippingInfo, validatePaymentInfo } from '../utils/validation';

const Checkout = () => {
    const navigate = useNavigate();
    const { cart, clearCart, getCartTotal } = useCart();
    const { user } = useAuth();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [validationErrors, setValidationErrors] = useState({
        shipping: {},
        payment: {}
    });
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        address: '',
        unit: '',
        city: '',
        province: '',
        zip_code: '',
        cardNumber: '',
        expiryDate: '',
        cvv: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        
        // Special handling for expiry date
        if (name === 'expiryDate') {
            // Remove any non-digit characters
            const digits = value.replace(/\D/g, '');
            let formattedValue = digits;
            
            // Add slash after first two digits if we have more than 2 digits
            if (digits.length > 2) {
                formattedValue = digits.slice(0, 2) + '/' + digits.slice(2);
            }
            
            setFormData(prevState => ({
                ...prevState,
                [name]: formattedValue
            }));
        } else {
            setFormData(prevState => ({
                ...prevState,
                [name]: value
            }));
        }

        // Clear validation errors when user types
        if (name === 'zip_code' || name in validationErrors.shipping) {
            setValidationErrors(prev => ({
                ...prev,
                shipping: { ...prev.shipping, [name]: '' }
            }));
        }
        if (name in validationErrors.payment) {
            setValidationErrors(prev => ({
                ...prev,
                payment: { ...prev.payment, [name]: '' }
            }));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        if (!user) {
            setError('You must be logged in to place an order');
            setLoading(false);
            return;
        }

        // Validate shipping information
        const shippingValidation = validateShippingInfo(formData);
        if (!shippingValidation.isValid) {
            setValidationErrors(prev => ({
                ...prev,
                shipping: shippingValidation.errors
            }));
            setLoading(false);
            return;
        }

        // Validate payment information
        const paymentValidation = validatePaymentInfo(formData);
        if (!paymentValidation.isValid) {
            setValidationErrors(prev => ({
                ...prev,
                payment: paymentValidation.errors
            }));
            setLoading(false);
            return;
        }

        try {
            const orderData = {
                user_id: user.id,
                items: cart.map(item => ({
                    product_id: item.id,
                    quantity: item.quantity
                })),
                shippingDetails: {
                    firstName: formData.firstName,
                    lastName: formData.lastName,
                    email: formData.email,
                    address: formData.address,
                    city: formData.city,
                    province: formData.province,
                    zip_code: formData.zip_code,
                    unit: formData.unit || null,
                    country: "CAN"
                },
                paymentDetails: {
                    cardNumber: formData.cardNumber,
                    expiryDate: formData.expiryDate,
                    cvv: formData.cvv
                },
                total_price: getCartTotal()
            };

            await orderAPI.createOrder(orderData);
            clearCart();
            navigate('/order-confirmation');
        } catch (error) {
            // Handle the error response properly
            const errorMessage = error.response?.data?.detail;
            if (Array.isArray(errorMessage)) {
                // If it's an array of validation errors, format them nicely
                setError(errorMessage.map(err => err.msg).join(', '));
            } else {
                setError(errorMessage || 'Failed to process order');
            }
            console.error('Order error:', error);
        } finally {
            setLoading(false);
        }
    };

    if (cart.length === 0) {
        return (
            <div className="max-w-2xl mx-auto p-4 text-center">
                <h2 className="text-2xl font-bold mb-4">Your cart is empty</h2>
                <button
                    onClick={() => navigate('/products')}
                    className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
                >
                    Continue Shopping
                </button>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto p-4">
            <h1 className="text-3xl font-bold mb-8">Checkout</h1>

            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{error}</span>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Order Summary */}
                <div className="bg-white p-6 rounded-lg shadow-sm">
                    <h2 className="text-xl font-bold mb-4">Order Summary</h2>
                    <div className="space-y-4">
                        {cart.map((item) => (
                            <div key={item.id} className="flex justify-between">
                                <span>{item.name} x {item.quantity}</span>
                                <span>${(item.price * item.quantity).toFixed(2)}</span>
                            </div>
                        ))}
                        <div className="border-t pt-4">
                            <div className="flex justify-between font-bold">
                                <span>Total</span>
                                <span>${getCartTotal().toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Shipping Information */}
                <div className="bg-white p-6 rounded-lg shadow-sm">
                    <h2 className="text-xl font-bold mb-4">Shipping Information</h2>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">First Name</label>
                                <input
                                    type="text"
                                    name="firstName"
                                    value={formData.firstName}
                                    onChange={handleChange}
                                    className={`mt-1 block w-full rounded-md ${
                                        validationErrors.shipping.firstName ? 'border-red-300' : 'border-gray-300'
                                    } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                    required
                                />
                                {validationErrors.shipping.firstName && (
                                    <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.firstName}</p>
                                )}
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Last Name</label>
                                <input
                                    type="text"
                                    name="lastName"
                                    value={formData.lastName}
                                    onChange={handleChange}
                                    className={`mt-1 block w-full rounded-md ${
                                        validationErrors.shipping.lastName ? 'border-red-300' : 'border-gray-300'
                                    } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                    required
                                />
                                {validationErrors.shipping.lastName && (
                                    <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.lastName}</p>
                                )}
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className={`mt-1 block w-full rounded-md ${
                                    validationErrors.shipping.email ? 'border-red-300' : 'border-gray-300'
                                } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                required
                            />
                            {validationErrors.shipping.email && (
                                <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.email}</p>
                            )}
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Address</label>
                            <input
                                type="text"
                                name="address"
                                value={formData.address}
                                onChange={handleChange}
                                className={`mt-1 block w-full rounded-md ${
                                    validationErrors.shipping.address ? 'border-red-300' : 'border-gray-300'
                                } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                required
                            />
                            {validationErrors.shipping.address && (
                                <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.address}</p>
                            )}
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">Unit Number (Optional)</label>
                            <input
                                type="text"
                                name="unit"
                                value={formData.unit}
                                onChange={handleChange}
                                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                placeholder="Apt 123"
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">City</label>
                                <input
                                    type="text"
                                    name="city"
                                    value={formData.city}
                                    onChange={handleChange}
                                    className={`mt-1 block w-full rounded-md ${
                                        validationErrors.shipping.city ? 'border-red-300' : 'border-gray-300'
                                    } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                    required
                                />
                                {validationErrors.shipping.city && (
                                    <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.city}</p>
                                )}
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Province</label>
                                <input
                                    type="text"
                                    name="province"
                                    value={formData.province}
                                    onChange={handleChange}
                                    className={`mt-1 block w-full rounded-md ${
                                        validationErrors.shipping.province ? 'border-red-300' : 'border-gray-300'
                                    } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                    required
                                />
                                {validationErrors.shipping.province && (
                                    <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.province}</p>
                                )}
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700">ZIP Code</label>
                            <input
                                type="text"
                                name="zip_code"
                                value={formData.zip_code}
                                onChange={handleChange}
                                className={`mt-1 block w-full rounded-md ${
                                    validationErrors.shipping.zip_code ? 'border-red-300' : 'border-gray-300'
                                } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                placeholder="A1A 1A1"
                                required
                            />
                            {validationErrors.shipping.zip_code && (
                                <p className="mt-1 text-sm text-red-600">{validationErrors.shipping.zip_code}</p>
                            )}
                        </div>

                        {/* Payment Information */}
                        <div className="mt-8">
                            <h2 className="text-xl font-bold mb-4">Payment Information</h2>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700">Card Number</label>
                                    <input
                                        type="text"
                                        name="cardNumber"
                                        value={formData.cardNumber}
                                        onChange={handleChange}
                                        className={`mt-1 block w-full rounded-md ${
                                            validationErrors.payment.cardNumber ? 'border-red-300' : 'border-gray-300'
                                        } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                        placeholder="XXXX XXXX XXXX XXXX"
                                        maxLength={19}
                                        required
                                    />
                                    {validationErrors.payment.cardNumber && (
                                        <p className="mt-1 text-sm text-red-600">{validationErrors.payment.cardNumber}</p>
                                    )}
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">Expiry Date</label>
                                        <input
                                            type="text"
                                            name="expiryDate"
                                            placeholder="MM/YY"
                                            value={formData.expiryDate}
                                            onChange={handleChange}
                                            className={`mt-1 block w-full rounded-md ${
                                                validationErrors.payment.expiryDate ? 'border-red-300' : 'border-gray-300'
                                            } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                            maxLength={5}
                                            required
                                        />
                                        {validationErrors.payment.expiryDate && (
                                            <p className="mt-1 text-sm text-red-600">{validationErrors.payment.expiryDate}</p>
                                        )}
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700">CVV</label>
                                        <input
                                            type="text"
                                            name="cvv"
                                            value={formData.cvv}
                                            onChange={handleChange}
                                            className={`mt-1 block w-full rounded-md ${
                                                validationErrors.payment.cvv ? 'border-red-300' : 'border-gray-300'
                                            } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                                            placeholder="123"
                                            maxLength={3}
                                            required
                                        />
                                        {validationErrors.payment.cvv && (
                                            <p className="mt-1 text-sm text-red-600">{validationErrors.payment.cvv}</p>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                                loading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                        >
                            {loading ? 'Processing...' : 'Place Order'}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Checkout;