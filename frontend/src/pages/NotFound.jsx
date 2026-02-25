import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div className="min-h-screen flex items-center justify-center px-4">
            <div className="max-w-xl text-center">
                <h1 className="text-9xl font-bold text-blue-600">404</h1>
                <h2 className="text-2xl font-semibold text-gray-900 mt-4">Page Not Found</h2>
                <p className="mt-4 text-gray-600">Sorry, we couldn't find the page you're looking for.</p>
                <div className="mt-8">
                    <Link
                        to="/"
                        className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors duration-200"
                    >
                        Go back home
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default NotFound;