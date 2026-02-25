import React, { useState, useEffect } from 'react';
import { userAPI, contactAPI } from '../services/api.service';
import { validateEmail, validatePassword } from '../utils/validation';

const AdminDashboard = () => {
    const [users, setUsers] = useState([]);
    const [contacts, setContacts] = useState([]);
    const [newUser, setNewUser] = useState({ email: '', password: '' });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [loading, setLoading] = useState(true);
    const [validationErrors, setValidationErrors] = useState({
        email: '',
        password: ''
    });

    useEffect(() => {
        fetchUsers();
        fetchContacts();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await userAPI.getAllUsers();
            setUsers(response);
            setLoading(false);
        } catch (error) {
            setError('Failed to fetch users');
            setLoading(false);
            console.error('Error fetching users:', error);
        }
    };

    const fetchContacts = async () => {
        try {
            const response = await contactAPI.getContacts();
            setContacts(response);
        } catch (error) {
            console.error('Error fetching contacts:', error);
        }
    };

    const handleNewUserChange = (e) => {
        const { name, value } = e.target;
        setNewUser(prev => ({ ...prev, [name]: value }));

        if (name === 'email') {
            if (!validateEmail(value)) {
                setValidationErrors(prev => ({ ...prev, email: 'Please enter a valid email address' }));
            } else {
                setValidationErrors(prev => ({ ...prev, email: '' }));
            }
        } else if (name === 'password') {
            const passwordValidation = validatePassword(value);
            setValidationErrors(prev => ({ ...prev, password: passwordValidation.message }));
        }
    };

    const handleCreateUser = async (e) => {
        e.preventDefault();
        setError('');

        // Validate email
        if (!validateEmail(newUser.email)) {
            setValidationErrors(prev => ({ ...prev, email: 'Please enter a valid email address' }));
            return;
        }

        // Validate password
        const passwordValidation = validatePassword(newUser.password);
        if (!passwordValidation.isValid) {
            setValidationErrors(prev => ({ ...prev, password: passwordValidation.message }));
            return;
        }

        try {
            await userAPI.createUser(newUser);
            setSuccess('User created successfully');
            setNewUser({ email: '', password: '' });
            setValidationErrors({ email: '', password: '' });
            // Refresh users list
            fetchUsers();
        } catch (error) {
            setError(error.response?.data?.detail || 'Failed to create user');
            console.error('Create user error:', error);
        }
    };

    const handleDeleteUser = async (userId) => {
        try {
            await userAPI.deleteUser(userId);
            setUsers(users.filter(user => user.id !== userId));
            setSuccess('User deleted successfully');
        } catch (error) {
            setError('Failed to delete user');
            console.error('Error deleting user:', error);
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto p-4">
            <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>
            
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{error}</span>
                </div>
            )}
            
            {success && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4">
                    <span className="block sm:inline">{success}</span>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Create User Form */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-xl font-bold mb-4">Create New User</h2>
                    <form onSubmit={handleCreateUser} className="space-y-4">
                        <div>
                            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                                Email
                            </label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={newUser.email}
                                onChange={handleNewUserChange}
                                className={`mt-1 block w-full border ${
                                    validationErrors.email ? 'border-red-300' : 'border-gray-300'
                                } rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500`}
                                required
                            />
                            {validationErrors.email && (
                                <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
                            )}
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                                Password
                            </label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                value={newUser.password}
                                onChange={handleNewUserChange}
                                className={`mt-1 block w-full border ${
                                    validationErrors.password ? 'border-red-300' : 'border-gray-300'
                                } rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500`}
                                required
                            />
                            {validationErrors.password && (
                                <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
                            )}
                        </div>
                        <button
                            type="submit"
                            disabled={!!validationErrors.email || !!validationErrors.password}
                            className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                                validationErrors.email || validationErrors.password
                                    ? 'bg-gray-400 cursor-not-allowed'
                                    : 'bg-blue-600 hover:bg-blue-700'
                            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                        >
                            Create User
                        </button>
                    </form>
                </div>

                {/* Users List */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-xl font-bold mb-4">Registered Users</h2>
                    {users.length === 0 ? (
                        <p className="text-gray-500">No users found</p>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Email
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Role
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Actions
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {users.map((user) => (
                                        <tr key={user.id}>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {user.email}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {user.is_admin ? 'Admin' : 'User'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                <button
                                                    onClick={() => handleDeleteUser(user.id)}
                                                    className="text-red-600 hover:text-red-900"
                                                >
                                                    Delete
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>

            {/* Contact Form Submissions */}
            <div className="mt-8 bg-white shadow rounded-lg p-6">
                <h2 className="text-xl font-bold mb-4">Contact Form Submissions</h2>
                {contacts.length === 0 ? (
                    <p className="text-gray-500">No contact form submissions found</p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Email
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Message
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Date
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {contacts.map((contact) => (
                                    <tr key={contact.id}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                            {contact.email}
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-900">
                                            {contact.message}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {new Date(contact.created_at).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AdminDashboard;