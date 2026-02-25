import React, { useState, useEffect } from 'react';
import { productAPI } from '../services/api.service';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';

const Products = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [notification, setNotification] = useState(null);
    const { addToCart } = useCart();
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data = await productAPI.getProducts();
                setProducts(data);
            } catch (error) {
                setError('Failed to fetch products');
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    const handleAddToCart = (product) => {
        if (!isAuthenticated) {
            setNotification({
                type: 'warning',
                message: 'Please sign in to add items to your cart'
            });
            setTimeout(() => setNotification(null), 3000);
            return;
        }

        if (product.stock <= 0) {
            setNotification({
                type: 'warning',
                message: 'This item is out of stock'
            });
            setTimeout(() => setNotification(null), 3000);
            return;
        }

        addToCart({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1,
            stock: product.stock
        });
        setNotification({
            type: 'success',
            message: 'Item added to cart successfully!'
        });
        setTimeout(() => setNotification(null), 3000);
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container mx-auto px-4 py-8">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
                    {error}
                </div>
            </div>
        );
    }

    if (!products || products.length === 0) {
        return (
            <div className="container mx-auto px-4 py-8">
                <h1 className="text-3xl font-bold mb-8">Products</h1>
                <p className="text-gray-600 text-center">No products available.</p>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-4 py-8">
            {notification && (
                <div className={`mb-4 p-4 rounded ${
                    notification.type === 'success' 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-yellow-100 text-yellow-700'
                }`}>
                    {notification.message}
                </div>
            )}
            <h1 className="text-3xl font-bold mb-8">Our Products</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((product) => (
                    <div key={product.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                        {product.image_url && (
                            <img
                                src={product.image_url}
                                alt={product.name}
                                className="w-full h-48 object-cover"
                            />
                        )}
                        <div className="p-4">
                            <h2 className="text-xl font-semibold mb-2">{product.name}</h2>
                            <p className="text-gray-600 mb-4 line-clamp-2">{product.description}</p>
                            <div className="flex justify-between items-center">
                                <span className="text-lg font-bold">${product.price.toFixed(2)}</span>
                                <span className={`text-sm ${
                                    product.stock > 0 ? 'text-green-600' : 'text-red-600'
                                }`}>
                                    {product.stock > 0 ? `In stock: ${product.stock}` : 'Out of stock'}
                                </span>
                            </div>
                            <button
                                className={`mt-4 w-full py-2 px-4 rounded transition-colors ${
                                    product.stock > 0
                                        ? 'bg-blue-600 text-white hover:bg-blue-700'
                                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                }`}
                                onClick={() => handleAddToCart(product)}
                                disabled={product.stock === 0}
                            >
                                {product.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Products;