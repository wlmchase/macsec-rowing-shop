import re
from typing import Tuple, Dict, Any
from datetime import datetime

def validate_shipping_info(shipping_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate shipping information.
    Returns a tuple of (is_valid, error_message)
    """
    # First Name validation
    if not shipping_data.get('firstName', '').strip():
        return False, "First name is required"
    if not re.match(r'^[a-zA-Z\s]{2,50}$', shipping_data['firstName']):
        return False, "First name must be 2-50 characters and contain only letters and spaces"

    # Last Name validation
    if not shipping_data.get('lastName', '').strip():
        return False, "Last name is required"
    if not re.match(r'^[a-zA-Z\s]{2,50}$', shipping_data['lastName']):
        return False, "Last name must be 2-50 characters and contain only letters and spaces"

    # Email validation
    if not shipping_data.get('email', '').strip():
        return False, "Email is required"
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, shipping_data['email']):
        return False, "Invalid email format"

    # Address validation
    if not shipping_data.get('address', '').strip():
        return False, "Address is required"
    if len(shipping_data['address']) < 5 or len(shipping_data['address']) > 100:
        return False, "Address must be between 5 and 100 characters"

    # City validation
    if not shipping_data.get('city', '').strip():
        return False, "City is required"
    if not re.match(r'^[a-zA-Z\s]{2,50}$', shipping_data['city']):
        return False, "City must be 2-50 characters and contain only letters and spaces"

    # Province validation
    if not shipping_data.get('province', '').strip():
        return False, "Province is required"
    if not re.match(r'^[a-zA-Z\s]{2,50}$', shipping_data['province']):
        return False, "Province must be 2-50 characters and contain only letters and spaces"

    # ZIP Code validation (Canadian format)
    if not shipping_data.get('zip_code', '').strip():
        return False, "ZIP code is required"
    if not re.match(r'^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$', shipping_data['zip_code']):
        return False, "Please enter a valid Canadian ZIP code (e.g., A1A 1A1)"

    return True, ""

def validate_payment_info(payment_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate payment information.
    Returns a tuple of (is_valid, error_message)
    """
    # Card Number validation
    if not payment_data.get('cardNumber', '').strip():
        return False, "Card number is required"
    card_number = payment_data['cardNumber'].replace(' ', '')
    if not re.match(r'^\d{15,16}$', card_number):
        return False, "Card number must be 15 or 16 digits"

    # Expiry Date validation
    if not payment_data.get('expiryDate', '').strip():
        return False, "Expiry date is required"
    expiry_date = payment_data['expiryDate']
    if not re.match(r'^(0[1-9]|1[0-2])/([0-9]{2})$', expiry_date):
        return False, "Expiry date must be in MM/YY format"
    
    # Check if card is expired
    month, year = expiry_date.split('/')
    expiry = datetime(2000 + int(year), int(month), 1)
    if expiry < datetime.now():
        return False, "Card has expired"

    # CVV validation
    if not payment_data.get('cvv', '').strip():
        return False, "CVV is required"
    if not re.match(r'^\d{3}$', payment_data['cvv']):
        return False, "CVV must be exactly 3 digits"

    return True, ""

def validate_order_data(order_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate the entire order data including shipping and payment information.
    Returns a tuple of (is_valid, error_message)
    """
    # Check if required fields exist
    if 'shippingDetails' not in order_data:
        return False, "Shipping details are required"
    if 'paymentDetails' not in order_data:
        return False, "Payment details are required"

    # Validate shipping information
    is_valid_shipping, shipping_error = validate_shipping_info(order_data['shippingDetails'])
    if not is_valid_shipping:
        return False, shipping_error

    # Validate payment information
    is_valid_payment, payment_error = validate_payment_info(order_data['paymentDetails'])
    if not is_valid_payment:
        return False, payment_error

    # Validate items
    if not order_data.get('items') or not isinstance(order_data['items'], list):
        return False, "Order must contain at least one item"
    
    return True, "" 