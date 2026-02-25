import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-[calc(100vh-16rem)] bg-gray-50">
            <h1 className="text-4xl font-bold text-gray-900 mb-6">
                Welcome to Rowing Shop
            </h1>
            <p className="text-lg text-gray-600 mb-8 text-center max-w-2xl px-4">
                CS617 - Software Security Project
            </p>
            <div className="flex gap-4">
                <Link
                    to="/products"
                    className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                    Browse Products
                </Link>
            </div>
        </div>
    );
};

export default Home;