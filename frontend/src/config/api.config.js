export const API_BASE_URL = 'http://localhost:8000/api';

export const API_ENDPOINTS = {
    // Auth endpoints
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH_TOKEN: '/auth/refresh',
    
    // User endpoints
    USER_PROFILE: '/users/me',
    UPDATE_PROFILE: '/users/me',
    ALL_USERS: '/users',
    
    // Product endpoints
    PRODUCTS: '/products',
    PRODUCT_DETAIL: (id) => `/products/${id}`,
    
    // Order endpoints
    ORDERS: '/orders',
    ORDER_DETAIL: (id) => `/orders/${id}`,
    
    // Contact form
    CONTACT: '/contact'
}; 