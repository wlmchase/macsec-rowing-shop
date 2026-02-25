export const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
};

export const validatePassword = (password) => {
    if (password.length < 12) {
        return {
            isValid: false,
            message: 'Password must be at least 12 characters long'
        };
    }

    if (password.length > 64) {
        return {
            isValid: false,
            message: 'Password must not exceed 64 characters'
        };
    }

    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasDigit = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (!hasLower || !hasUpper || !hasDigit || !hasSpecial) {
        return {
            isValid: false,
            message: 'Password must contain at least one lowercase letter, one uppercase letter, one number, and one special character'
        };
    }

    return {
        isValid: true,
        message: ''
    };
};

export const validateShippingInfo = (formData) => {
    const errors = {};

    // First Name validation
    if (!formData.firstName.trim()) {
        errors.firstName = 'First name is required';
    } else if (!/^[a-zA-Z\s-']{2,50}$/.test(formData.firstName)) {
        errors.firstName = 'First name must be 2-50 characters and contain only letters, spaces, hyphens, and apostrophes';
    }

    // Last Name validation
    if (!formData.lastName.trim()) {
        errors.lastName = 'Last name is required';
    } else if (!/^[a-zA-Z\s-']{2,50}$/.test(formData.lastName)) {
        errors.lastName = 'Last name must be 2-50 characters and contain only letters, spaces, hyphens, and apostrophes';
    }

    // Email validation
    if (!validateEmail(formData.email)) {
        errors.email = 'Please enter a valid email address';
    }

    // Address validation
    if (!formData.address.trim()) {
        errors.address = 'Address is required';
    } else if (formData.address.length < 5 || formData.address.length > 100) {
        errors.address = 'Address must be between 5 and 100 characters';
    }

    // City validation
    if (!formData.city.trim()) {
        errors.city = 'City is required';
    } else if (!/^[a-zA-Z\s-']{2,50}$/.test(formData.city)) {
        errors.city = 'City must be 2-50 characters and contain only letters, spaces, hyphens, and apostrophes';
    }

    // Province validation
    if (!formData.province.trim()) {
        errors.province = 'Province is required';
    } else if (!/^[a-zA-Z\s-']{2,50}$/.test(formData.province)) {
        errors.province = 'Province must be 2-50 characters and contain only letters, spaces, hyphens, and apostrophes';
    }

    // ZIP Code validation (Canadian format)
    if (!formData.zip_code.trim()) {
        errors.zip_code = 'ZIP code is required';
    } else if (!/^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$/.test(formData.zip_code)) {
        errors.zip_code = 'Please enter a valid Canadian ZIP code (e.g., A1A 1A1)';
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
};

export const validatePaymentInfo = (formData) => {
    const errors = {};

    // Card Number validation
    if (!formData.cardNumber.trim()) {
        errors.cardNumber = 'Card number is required';
    } else if (!/^\d{15,16}$/.test(formData.cardNumber.replace(/\s/g, ''))) {
        errors.cardNumber = 'Card number must be 15 or 16 digits';
    }

    // Expiry Date validation
    if (!formData.expiryDate.trim()) {
        errors.expiryDate = 'Expiry date is required';
    } else {
        const expiryRegex = /^(0[1-9]|1[0-2])\/([0-9]{2})$/;
        if (!expiryRegex.test(formData.expiryDate)) {
            errors.expiryDate = 'Expiry date must be in MM/YY format';
        } else {
            const [month, year] = formData.expiryDate.split('/');
            const expiry = new Date(2000 + parseInt(year), parseInt(month) - 1);
            if (expiry < new Date()) {
                errors.expiryDate = 'Card has expired';
            }
        }
    }

    // CVV validation
    if (!formData.cvv.trim()) {
        errors.cvv = 'CVV is required';
    } else if (!/^\d{3}$/.test(formData.cvv)) {
        errors.cvv = 'CVV must be exactly 3 digits';
    }

    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
}; 