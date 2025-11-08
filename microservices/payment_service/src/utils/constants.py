"""
Constants and Enums for Payment Service
Centralized constants and enumerations
"""
from enum import Enum
from typing import List

class PaymentStatus(Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class PaymentMethod(Enum):
    """Payment method enumeration"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"

class Currency(Enum):
    """Supported currencies"""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"

class EventType(Enum):
    """RabbitMQ event types"""
    PAYMENT_REQUEST = "payment.request"
    PAYMENT_RESPONSE = "payment.response"
    PAYMENT_COMPLETED = "payment.completed"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_REFUNDED = "payment.refunded"

class APIResponseStatus(Enum):
    """API response status enumeration"""
    SUCCESS = "success"
    ERROR = "error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INTERNAL_ERROR = "internal_error"

class PaymentConstants:
    """Payment-related constants"""
    
    # Amount limits
    MIN_AMOUNT = 0.01
    MAX_AMOUNT = 1000000.00
    
    # Card validation
    MIN_CARD_LENGTH = 13
    MAX_CARD_LENGTH = 19
    MIN_CVV_LENGTH = 3
    MAX_CVV_LENGTH = 4
    
    # Processing timeouts
    PAYMENT_TIMEOUT = 30  # seconds
    REFUND_TIMEOUT = 60   # seconds
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 100  # requests per minute
    RATE_LIMIT_WINDOW = 60     # seconds

class ErrorMessages:
    """Standardized error messages"""
    
    # Validation errors
    INVALID_AMOUNT = "Invalid amount provided"
    INVALID_CURRENCY = "Unsupported currency"
    INVALID_PAYMENT_METHOD = "Invalid payment method"
    INVALID_CARD_NUMBER = "Invalid card number"
    INVALID_CVV = "Invalid CVV"
    INVALID_EXPIRY_DATE = "Invalid expiry date"
    CARD_EXPIRED = "Card has expired"
    MISSING_REQUIRED_FIELD = "Missing required field: {field}"
    
    # Business logic errors
    PAYMENT_NOT_FOUND = "Payment not found"
    PAYMENT_ALREADY_PROCESSED = "Payment already processed"
    PAYMENT_CANNOT_BE_REFUNDED = "Payment cannot be refunded"
    INSUFFICIENT_FUNDS = "Insufficient funds"
    PAYMENT_DECLINED = "Payment declined by gateway"
    
    # System errors
    INTERNAL_ERROR = "Internal server error"
    SERVICE_UNAVAILABLE = "Service temporarily unavailable"
    TIMEOUT_ERROR = "Request timeout"
    RATE_LIMIT_EXCEEDED = "Rate limit exceeded"
    
    # Authentication errors
    UNAUTHORIZED = "Unauthorized access"
    INVALID_TOKEN = "Invalid authentication token"
    TOKEN_EXPIRED = "Authentication token expired"

class SuccessMessages:
    """Standardized success messages"""
    
    PAYMENT_PROCESSED = "Payment processed successfully"
    PAYMENT_REFUNDED = "Payment refunded successfully"
    PAYMENT_METHOD_VALID = "Payment method is valid"
    PAYMENT_STATUS_RETRIEVED = "Payment status retrieved successfully"
    USER_PAYMENTS_RETRIEVED = "User payments retrieved successfully"

class LogMessages:
    """Standardized log messages"""
    
    # Info messages
    SERVICE_STARTED = "Payment Service started on port {port}"
    CONSUMER_STARTED = "RabbitMQ consumer started"
    PAYMENT_PROCESSED = "Payment {payment_id} processed with status: {status}"
    PAYMENT_REFUNDED = "Payment {payment_id} refunded successfully"
    EVENT_PUBLISHED = "Published payment event: {event_type}"
    
    # Error messages
    CONSUMER_ERROR = "Error starting consumer: {error}"
    PAYMENT_ERROR = "Error processing payment: {error}"
    EVENT_PUBLISH_ERROR = "Error publishing payment event: {error}"
    VALIDATION_ERROR = "Validation error: {error}"
    DATABASE_ERROR = "Database error: {error}"
    RABBITMQ_ERROR = "RabbitMQ error: {error}"

class HTTPStatusCodes:
    """HTTP status codes"""
    
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

