"""
Payment API Routes
REST endpoints for payment operations with improved error handling and validation
"""
from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService
from events.payment_producer import PaymentProducer
from utils.validators import PaymentValidator
from utils.api_response import ResponseBuilder, ErrorHandler, ResponseFormatter
from utils.constants import HTTPStatusCodes, ErrorMessages, SuccessMessages
import logging

logger = logging.getLogger(__name__)
payment_bp = Blueprint('payment', __name__)
payment_service = PaymentService()
payment_producer = PaymentProducer()

@payment_bp.route('/', methods=['POST'])
def create_payment():
    """
    Create a new payment with comprehensive validation and error handling
    
    Request body:
    {
        "order_id": "string",
        "user_id": "string", 
        "amount": float,
        "currency": "USD",
        "payment_method": "credit_card"
    }
    
    Returns:
        JSON response with payment result
    """
    try:
        # Get and validate request data
        data = request.get_json()
        if not data:
            response = ResponseBuilder.validation_error(
                message="No data provided",
                errors=[{"field": "body", "message": "Request body is required"}]
            )
            return response.to_json_response()
        
        # Validate payment data
        is_valid, validation_errors = PaymentValidator.validate_payment_request(data)
        if not is_valid:
            response = ResponseBuilder.validation_error(
                message="Validation failed",
                errors=[{"field": "validation", "message": error} for error in validation_errors]
            )
            return response.to_json_response()
        
        # Process payment
        result = payment_service.process_payment(data)
        
        # Publish payment event based on status
        try:
            if result['status'] == 'completed':
                payment_producer.publish_payment_event('completed', result)
            elif result['status'] == 'failed':
                payment_producer.publish_payment_event('failed', result)
        except Exception as e:
            logger.warning(f"Failed to publish payment event: {str(e)}")
            # Don't fail the request if event publishing fails
        
        # Return appropriate response
        if result['status'] in ['completed', 'pending']:
            response = ResponseBuilder.success(
                message=SuccessMessages.PAYMENT_PROCESSED,
                data=ResponseFormatter.format_payment_response(result)
            )
            return response.to_json_response()
        else:
            response = ResponseBuilder.error(
                message=result.get('message', ErrorMessages.PAYMENT_DECLINED),
                errors=result.get('errors', []),
                status_code=HTTPStatusCodes.BAD_REQUEST
            )
            return response.to_json_response()
        
    except Exception as e:
        logger.error(f"Error in create_payment: {str(e)}")
        response = ErrorHandler.handle_payment_error(e)
        return response.to_json_response()

@payment_bp.route('/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    """
    Get payment status by ID with improved error handling
    
    Args:
        payment_id: Payment identifier
        
    Returns:
        JSON response with payment details or error
    """
    try:
        if not payment_id:
            response = ResponseBuilder.validation_error(
                message="Payment ID is required",
                errors=[{"field": "payment_id", "message": "Payment ID cannot be empty"}]
            )
            return response.to_json_response()
        
        result = payment_service.get_payment_status(payment_id)
        
        if result:
            response = ResponseBuilder.success(
                message=SuccessMessages.PAYMENT_STATUS_RETRIEVED,
                data=ResponseFormatter.format_payment_response(result)
            )
            return response.to_json_response()
        else:
            response = ResponseBuilder.not_found(
                message=ErrorMessages.PAYMENT_NOT_FOUND
            )
            return response.to_json_response()
            
    except Exception as e:
        logger.error(f"Error in get_payment: {str(e)}")
        response = ErrorHandler.handle_payment_error(e, payment_id)
        return response.to_json_response()

@payment_bp.route('/user/<user_id>', methods=['GET'])
def get_user_payments(user_id):
    """
    Get all payments for a user with improved error handling
    
    Args:
        user_id: User identifier
        
    Returns:
        JSON response with user payments or error
    """
    try:
        if not user_id:
            response = ResponseBuilder.validation_error(
                message="User ID is required",
                errors=[{"field": "user_id", "message": "User ID cannot be empty"}]
            )
            return response.to_json_response()
        
        payments = payment_service.get_user_payments(user_id)
        
        response = ResponseBuilder.success(
            message=SuccessMessages.USER_PAYMENTS_RETRIEVED,
            data=ResponseFormatter.format_payment_list(payments)
        )
        return response.to_json_response()
        
    except Exception as e:
        logger.error(f"Error in get_user_payments: {str(e)}")
        response = ErrorHandler.handle_payment_error(e, user_id)
        return response.to_json_response()

@payment_bp.route('/<payment_id>/refund', methods=['POST'])
def refund_payment(payment_id):
    """
    Refund a payment with improved validation and error handling
    
    Args:
        payment_id: Payment identifier to refund
        
    Returns:
        JSON response with refund result or error
    """
    try:
        if not payment_id:
            response = ResponseBuilder.validation_error(
                message="Payment ID is required",
                errors=[{"field": "payment_id", "message": "Payment ID cannot be empty"}]
            )
            return response.to_json_response()
        
        result = payment_service.refund_payment(payment_id)
        
        if result['success']:
            # Publish refund event
            try:
                payment_producer.publish_payment_event('refunded', {
                    'payment_id': payment_id,
                    'refunded_at': result.get('refunded_at')
                })
            except Exception as e:
                logger.warning(f"Failed to publish refund event: {str(e)}")
                # Don't fail the request if event publishing fails
            
            response = ResponseBuilder.success(
                message=result['message'],
                data=result
            )
            return response.to_json_response()
        else:
            response = ResponseBuilder.error(
                message=result['message'],
                errors=result.get('errors', []),
                status_code=HTTPStatusCodes.BAD_REQUEST
            )
            return response.to_json_response()
            
    except Exception as e:
        logger.error(f"Error in refund_payment: {str(e)}")
        response = ErrorHandler.handle_payment_error(e, payment_id)
        return response.to_json_response()

@payment_bp.route('/validate', methods=['POST'])
def validate_payment_method():
    """
    Validate payment method with comprehensive validation
    
    Request body:
    {
        "card_number": "string",
        "cvv": "string", 
        "expiry_date": "MM/YY"
    }
    
    Returns:
        JSON response with validation result
    """
    try:
        data = request.get_json()
        if not data:
            response = ResponseBuilder.validation_error(
                message="No data provided",
                errors=[{"field": "body", "message": "Request body is required"}]
            )
            return response.to_json_response()
        
        # Validate payment method data
        is_valid, validation_errors = PaymentValidator.validate_payment_method(data)
        
        if is_valid:
            response = ResponseBuilder.success(
                message=SuccessMessages.PAYMENT_METHOD_VALID,
                data={'valid': True}
            )
            return response.to_json_response()
        else:
            response = ResponseBuilder.validation_error(
                message="Payment method validation failed",
                errors=[{"field": "validation", "message": error} for error in validation_errors]
            )
            return response.to_json_response()
            
    except Exception as e:
        logger.error(f"Error in validate_payment_method: {str(e)}")
        response = ErrorHandler.handle_payment_error(e)
        return response.to_json_response()

