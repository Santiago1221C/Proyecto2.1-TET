"""
Validators module for Payment Service
Centralized validation logic for input data
"""
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)

class PaymentValidator:
    """Validator for payment-related data"""
    
    @staticmethod
    def validate_payment_request(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate payment request data
        
        Args:
            data: Payment request data dictionary
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Required fields validation
        required_fields = ['order_id', 'user_id', 'amount']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Field '{field}' is required")
        
        # Amount validation
        if 'amount' in data:
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    errors.append("Amount must be greater than 0")
                if amount > 1000000:  # Max amount limit
                    errors.append("Amount exceeds maximum limit")
            except (ValueError, TypeError):
                errors.append("Amount must be a valid number")
        
        # Currency validation
        if 'currency' in data:
            valid_currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
            if data['currency'] not in valid_currencies:
                errors.append(f"Currency must be one of: {', '.join(valid_currencies)}")
        
        # Payment method validation
        if 'payment_method' in data:
            valid_methods = ['credit_card', 'debit_card', 'paypal', 'bank_transfer']
            if data['payment_method'] not in valid_methods:
                errors.append(f"Payment method must be one of: {', '.join(valid_methods)}")
        
        # Order ID format validation
        if 'order_id' in data and data['order_id']:
            if not re.match(r'^[A-Za-z0-9_-]+$', data['order_id']):
                errors.append("Order ID must contain only alphanumeric characters, hyphens, and underscores")
        
        # User ID format validation
        if 'user_id' in data and data['user_id']:
            if not re.match(r'^[A-Za-z0-9_-]+$', data['user_id']):
                errors.append("User ID must contain only alphanumeric characters, hyphens, and underscores")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_payment_method(data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate payment method data
        
        Args:
            data: Payment method data dictionary
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Required fields
        required_fields = ['card_number', 'cvv', 'expiry_date']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Field '{field}' is required")
        
        # Card number validation
        if 'card_number' in data and data['card_number']:
            card_number = data['card_number'].replace(' ', '').replace('-', '')
            if not re.match(r'^\d{13,19}$', card_number):
                errors.append("Card number must be 13-19 digits")
            
            # Luhn algorithm validation
            if not PaymentValidator._luhn_check(card_number):
                errors.append("Invalid card number")
        
        # CVV validation
        if 'cvv' in data and data['cvv']:
            if not re.match(r'^\d{3,4}$', data['cvv']):
                errors.append("CVV must be 3-4 digits")
        
        # Expiry date validation
        if 'expiry_date' in data and data['expiry_date']:
            if not re.match(r'^\d{2}/\d{2}$', data['expiry_date']):
                errors.append("Expiry date must be in MM/YY format")
            else:
                try:
                    month, year = data['expiry_date'].split('/')
                    month = int(month)
                    year = int('20' + year)
                    
                    if month < 1 or month > 12:
                        errors.append("Invalid month in expiry date")
                    
                    current_date = datetime.now()
                    if year < current_date.year or (year == current_date.year and month < current_date.month):
                        errors.append("Card has expired")
                except ValueError:
                    errors.append("Invalid expiry date format")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _luhn_check(card_number: str) -> bool:
        """
        Luhn algorithm for card number validation
        
        Args:
            card_number: Card number string
            
        Returns:
            True if valid, False otherwise
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0

class APIResponseValidator:
    """Validator for API response data"""
    
    @staticmethod
    def validate_response_structure(response: Dict) -> bool:
        """
        Validate API response structure
        
        Args:
            response: API response dictionary
            
        Returns:
            True if valid structure, False otherwise
        """
        required_fields = ['status', 'message']
        return all(field in response for field in required_fields)
    
    @staticmethod
    def sanitize_response_data(data: Dict) -> Dict:
        """
        Sanitize response data to remove sensitive information
        
        Args:
            data: Response data dictionary
            
        Returns:
            Sanitized data dictionary
        """
        sensitive_fields = ['card_number', 'cvv', 'password', 'secret']
        sanitized = data.copy()
        
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = '***'
        
        return sanitized

