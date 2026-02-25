import React from 'react';
import { Link } from 'react-router-dom';

const OrderConfirmation = () => {
    return (
        <div className="max-w-2xl mx-auto p-4">
            <div className="bg-white shadow-sm rounded-lg p-8 text-center">
                <div className="mb-6">
                    <svg
                        className="mx-auto h-12 w-12 text-green-500"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                        <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                        />
                    </svg>
                </div>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">
                    Order Placed Successfully!
                </h1>
                <div className="flex justify-center">
                    <Link
                        to="/products"
                        className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition-colors"
                    >
                        Continue Shopping
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default OrderConfirmation; 