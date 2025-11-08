"""
API Response utilities for Payment Service
Standardized response formatting and error handling
"""
from typing import Dict, Any, Optional, Union
from datetime import datetime
import logging
from .constants import APIResponseStatus, ErrorMessages, SuccessMessages, HTTPStatusCodes

logger = logging.getLogger(__name__)

class APIResponse:
    """Standardized API response class"""
    
    def __init__(self, status: APIResponseStatus, message: str, data: Optional[Dict] = None, 
                 errors: Optional[list] = None, status_code: Optional[int] = None):
        """
        Initialize API response
        
        Args:
            status: Response status
            message: Response message
            data: Response data (optional)
            errors: List of errors (optional)
            status_code: HTTP status code (optional)
        """
        self.status = status
        self.message = message
        self.data = data or {}
        self.errors = errors or []
        self.status_code = status_code or self._get_default_status_code()
        self.timestamp = datetime.utcnow().isoformat()
    
    def _get_default_status_code(self) -> int:
        """Get default HTTP status code based on response status"""
        status_mapping = {
            APIResponseStatus.SUCCESS: HTTPStatusCodes.OK,
            APIResponseStatus.ERROR: HTTPStatusCodes.INTERNAL_SERVER_ERROR,
            APIResponseStatus.VALIDATION_ERROR: HTTPStatusCodes.BAD_REQUEST,
            APIResponseStatus.NOT_FOUND: HTTPStatusCodes.NOT_FOUND,
            APIResponseStatus.UNAUTHORIZED: HTTPStatusCodes.UNAUTHORIZED,
            APIResponseStatus.FORBIDDEN: HTTPStatusCodes.FORBIDDEN,
            APIResponseStatus.INTERNAL_ERROR: HTTPStatusCodes.INTERNAL_SERVER_ERROR
        }
        return status_mapping.get(self.status, HTTPStatusCodes.INTERNAL_SERVER_ERROR)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary"""
        response = {
            'status': self.status.value,
            'message': self.message,
            'timestamp': self.timestamp,
            'data': self.data
        }
        
        if self.errors:
            response['errors'] = self.errors
        
        return response
    
    def to_json_response(self) -> tuple:
        """Convert to Flask JSON response tuple"""
        return self.to_dict(), self.status_code

class ResponseBuilder:
    """Builder class for creating standardized responses"""
    
    @staticmethod
    def success(message: str = SuccessMessages.PAYMENT_PROCESSED, 
                data: Optional[Dict] = None, 
                status_code: int = HTTPStatusCodes.OK) -> APIResponse:
        """Create success response"""
        return APIResponse(
            status=APIResponseStatus.SUCCESS,
            message=message,
            data=data,
            status_code=status_code
        )
    
    @staticmethod
    def error(message: str = ErrorMessages.INTERNAL_ERROR, 
              errors: Optional[list] = None,
              status_code: int = HTTPStatusCodes.INTERNAL_SERVER_ERROR) -> APIResponse:
        """Create error response"""
        return APIResponse(
            status=APIResponseStatus.ERROR,
            message=message,
            errors=errors,
            status_code=status_code
        )
    
    @staticmethod
    def validation_error(message: str = ErrorMessages.MISSING_REQUIRED_FIELD, 
                        errors: Optional[list] = None) -> APIResponse:
        """Create validation error response"""
        return APIResponse(
            status=APIResponseStatus.VALIDATION_ERROR,
            message=message,
            errors=errors,
            status_code=HTTPStatusCodes.BAD_REQUEST
        )
    
    @staticmethod
    def not_found(message: str = ErrorMessages.PAYMENT_NOT_FOUND) -> APIResponse:
        """Create not found response"""
        return APIResponse(
            status=APIResponseStatus.NOT_FOUND,
            message=message,
            status_code=HTTPStatusCodes.NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(message: str = ErrorMessages.UNAUTHORIZED) -> APIResponse:
        """Create unauthorized response"""
        return APIResponse(
            status=APIResponseStatus.UNAUTHORIZED,
            message=message,
            status_code=HTTPStatusCodes.UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(message: str = ErrorMessages.UNAUTHORIZED) -> APIResponse:
        """Create forbidden response"""
        return APIResponse(
            status=APIResponseStatus.FORBIDDEN,
            message=message,
            status_code=HTTPStatusCodes.FORBIDDEN
        )
    
    @staticmethod
    def internal_error(message: str = ErrorMessages.INTERNAL_ERROR, 
                      errors: Optional[list] = None) -> APIResponse:
        """Create internal error response"""
        return APIResponse(
            status=APIResponseStatus.INTERNAL_ERROR,
            message=message,
            errors=errors,
            status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR
        )

class ErrorHandler:
    """Error handling utilities"""
    
    @staticmethod
    def handle_validation_error(errors: list) -> APIResponse:
        """Handle validation errors"""
        logger.warning(f"Validation error: {errors}")
        return ResponseBuilder.validation_error(
            message="Validation failed",
            errors=errors
        )
    
    @staticmethod
    def handle_payment_error(error: Exception, payment_id: Optional[str] = None) -> APIResponse:
        """Handle payment processing errors"""
        logger.error(f"Payment error for {payment_id}: {str(error)}")
        return ResponseBuilder.error(
            message=ErrorMessages.PAYMENT_DECLINED,
            errors=[str(error)]
        )
    
    @staticmethod
    def handle_database_error(error: Exception) -> APIResponse:
        """Handle database errors"""
        logger.error(f"Database error: {str(error)}")
        return ResponseBuilder.internal_error(
            message=ErrorMessages.INTERNAL_ERROR,
            errors=["Database operation failed"]
        )
    
    @staticmethod
    def handle_rabbitmq_error(error: Exception) -> APIResponse:
        """Handle RabbitMQ errors"""
        logger.error(f"RabbitMQ error: {str(error)}")
        return ResponseBuilder.internal_error(
            message=ErrorMessages.SERVICE_UNAVAILABLE,
            errors=["Message queue operation failed"]
        )
    
    @staticmethod
    def handle_timeout_error(error: Exception) -> APIResponse:
        """Handle timeout errors"""
        logger.error(f"Timeout error: {str(error)}")
        return ResponseBuilder.error(
            message=ErrorMessages.TIMEOUT_ERROR,
            status_code=HTTPStatusCodes.GATEWAY_TIMEOUT
        )

class ResponseFormatter:
    """Response formatting utilities"""
    
    @staticmethod
    def format_payment_response(payment_data: Dict) -> Dict:
        """Format payment data for API response"""
        return {
            'payment_id': payment_data.get('payment_id'),
            'order_id': payment_data.get('order_id'),
            'user_id': payment_data.get('user_id'),
            'amount': payment_data.get('amount'),
            'currency': payment_data.get('currency'),
            'status': payment_data.get('status'),
            'transaction_id': payment_data.get('transaction_id'),
            'message': payment_data.get('message'),
            'created_at': payment_data.get('created_at'),
            'updated_at': payment_data.get('updated_at')
        }
    
    @staticmethod
    def format_payment_list(payments: list) -> Dict:
        """Format payment list for API response"""
        return {
            'payments': [
                ResponseFormatter.format_payment_response(payment) 
                for payment in payments
            ],
            'total': len(payments)
        }
    
    @staticmethod
    def format_validation_errors(errors: list) -> list:
        """Format validation errors for API response"""
        return [
            {
                'field': error.get('field', 'unknown'),
                'message': error.get('message', error),
                'code': error.get('code', 'VALIDATION_ERROR')
            }
            for error in errors
        ]

