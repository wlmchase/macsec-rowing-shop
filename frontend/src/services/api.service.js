import axios from 'axios';
import { API_BASE_URL } from '../config/api.config';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // If the error is 401 and we haven't retried yet
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                // Try to refresh the token
                const refreshToken = localStorage.getItem('refresh_token');
                if (!refreshToken) {
                    throw new Error('No refresh token available');
                }

                const response = await axios.post(`${API_BASE_URL}/auth/refresh`, refreshToken, {
                    headers: {
                        'Content-Type': 'text/plain'
                    }
                });

                const { access_token } = response.data;
                localStorage.setItem('access_token', access_token);

                // Retry the original request
                originalRequest.headers.Authorization = `Bearer ${access_token}`;
                return api(originalRequest);
            } catch (error) {
                // If refresh token fails, logout user
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
                return Promise.reject(error);
            }
        }

        return Promise.reject(error);
    }
);

export const authAPI = {
    login: async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        
        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);
        return response.data;
    },

    register: async (data) => {
        const response = await api.post('/auth/register', data);
        return response.data;
    },

    logout: async () => {
        try {
            const token = localStorage.getItem('access_token');
            if (token) {
                await api.post('/auth/logout');
            }
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
        }
    },

    changePassword: async (currentPassword, newPassword) => {
        const response = await api.post('/auth/change-password', {
            current: currentPassword,
            new: newPassword
        });
        return response.data;
    }
};

export const userAPI = {
    getProfile: () => api.get('/users/me'),
    updateProfile: (data) => api.put('/users/me', data),
    getAllUsers: async () => {
        const response = await api.get('/users/all-users');
        return response.data;
    },
    createUser: async (data) => {
        const response = await api.post('/auth/register', data);
        return response.data;
    },
    updateUser: (id, data) => api.put(`/users/${id}`, data),
    deleteUser: (id) => api.delete(`/users/${id}`),
};

export const productAPI = {
    getProducts: async () => {
        const response = await api.get('/products');
        return response.data;
    },
    getProduct: async (id) => {
        const response = await api.get(`/products/${id}`);
        return response.data;
    },
    createProduct: async (data) => {
        const response = await api.post('/products', data);
        return response.data;
    },
    updateProduct: async (id, data) => {
        const response = await api.put(`/products/${id}`, data);
        return response.data;
    },
    deleteProduct: async (id) => {
        const response = await api.delete(`/products/${id}`);
        return response.data;
    },
};

export const orderAPI = {
    getOrders: (userId) => api.get(`/orders/user/${userId}`),
    getOrder: (id) => api.get(`/orders/${id}`),
    createOrder: (data) => api.post('/orders/place-order', {
        user_id: data.user_id,
        items: data.items.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity
        })),
        shippingDetails: data.shippingDetails,
        paymentDetails: data.paymentDetails
    }),
    updateOrder: (id, data) => api.put(`/orders/${id}`, data),
};

export const contactAPI = {
    submitForm: async (formData) => {
        const response = await api.post('/contact/', {
            email: formData.email,
            message: formData.message
        });
        return response.data;
    },
    getContacts: async () => {
        const response = await api.get('/contact/');
        return response.data;
    }
};

export default api; 