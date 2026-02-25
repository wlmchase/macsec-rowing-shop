import React, { useState } from 'react';
import { contactAPI } from '../services/api.service';

const Contact = () => {
    const [formData, setFormData] = useState({
        email: '',
        message: ''
    });
    const [status, setStatus] = useState({ type: '', message: '' });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name === 'message' && value.length > 300) {
            return;
        }
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setStatus({ type: '', message: '' });

        try {
            await contactAPI.submitForm(formData);
            setStatus({
                type: 'success',
                message: 'Thank you for your message. We will get back to you soon!'
            });
            setFormData({ email: '', message: '' });
        } catch (error) {
            setStatus({
                type: 'error',
                message: error.response?.data?.detail || 'There was an error sending your message. Please try again.'
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-4">
            <div className="text-center mb-8">
                <h1 className="text-3xl font-bold">Contact Us</h1>
                <p className="mt-2 text-gray-600">
                    Have a question? Send us a message!
                </p>
            </div>

            {status.message && (
                <div className={`mb-4 p-4 rounded ${
                    status.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                }`}>
                    {status.message}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6 bg-white shadow-sm rounded-lg p-6">
                <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                        Email
                    </label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        required
                    />
                </div>

                <div>
                    <div className="flex justify-between">
                        <label htmlFor="message" className="block text-sm font-medium text-gray-700">
                            Message
                        </label>
                        <span className="text-sm text-gray-500">
                            {formData.message.length}/300 characters
                        </span>
                    </div>
                    <textarea
                        id="message"
                        name="message"
                        rows="4"
                        value={formData.message}
                        onChange={handleChange}
                        maxLength={300}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        required
                    ></textarea>
                </div>

                <div>
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white ${
                            loading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                        } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                    >
                        {loading ? 'Sending...' : 'Send Message'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Contact;