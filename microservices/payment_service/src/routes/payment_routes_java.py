"""
Payment Service Java-style Routes (Flask implementation)
This provides Java Spring Boot style endpoints using Flask
"""

from flask import Blueprint, request, jsonify
from services.payment_service import PaymentService
from events.payment_producer import PaymentProducer
from utils.validators import PaymentValidator
from utils.api_response import ResponseBuilder, ErrorHandler, ResponseFormatter
from utils.constants import HTTPStatusCodes, ErrorMessages, SuccessMessages
import logging

logger = logging.getLogger(__name__)
payment_java_bp = Blueprint('payment_java', __name__)
payment_service = PaymentService()
payment_producer = PaymentProducer()

@payment_java_bp.route('/', methods=['POST'])
def create_payment_java_style():
    """
    Create a new payment (Java Spring Boot style endpoint)
    
    Request body:
    {
        "orderId": "string",
        "userId": "string", 
        "amount": float,
        "currency": "USD",
        "paymentMethod": "credit_card"
    }
    
    Returns:
        JSON response with payment result
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided',
                'errors': ['Request body is required']
            }), 400
        
        # Convert Java-style field names to Python-style
        payment_data = {
            'order_id': data.get('orderId'),
            'user_id': data.get('userId'),
            'amount': data.get('amount'),
            'currency': data.get('currency'),
            'payment_method': data.get('paymentMethod')
        }
        
        # Validate payment data
        is_valid, validation_errors = PaymentValidator.validate_payment_request(payment_data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': validation_errors
            }), 400
        
        # Process payment
        result = payment_service.process_payment(payment_data)
        
        # Publish payment event
        try:
            if result['status'] == 'completed':
                payment_producer.publish_payment_event('completed', result)
            elif result['status'] == 'failed':
                payment_producer.publish_payment_event('failed', result)
        except Exception as e:
            logger.warning(f"Failed to publish payment event: {str(e)}")
        
        # Return Java-style response
        if result['status'] in ['completed', 'pending']:
            return jsonify({
                'success': True,
                'message': 'Payment processed successfully',
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result.get('message', 'Payment declined'),
                'errors': result.get('errors', [])
            }), 400
        
    except Exception as e:
        logger.error(f"Error in create_payment_java_style: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': [str(e)]
        }), 500

@payment_java_bp.route('/<payment_id>', methods=['GET'])
def get_payment_java_style(payment_id):
    """
    Get payment status by ID (Java Spring Boot style)
    """
    try:
        if not payment_id:
            return jsonify({
                'success': False,
                'message': 'Payment ID is required',
                'errors': ['Payment ID cannot be empty']
            }), 400
        
        result = payment_service.get_payment_status(payment_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Payment retrieved successfully',
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Payment not found',
                'errors': ['Payment not found']
            }), 404
            
    except Exception as e:
        logger.error(f"Error in get_payment_java_style: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': [str(e)]
        }), 500

@payment_java_bp.route('/user/<user_id>', methods=['GET'])
def get_user_payments_java_style(user_id):
    """
    Get all payments for a user (Java Spring Boot style)
    """
    try:
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'User ID is required',
                'errors': ['User ID cannot be empty']
            }), 400
        
        payments = payment_service.get_user_payments(user_id)
        
        return jsonify({
            'success': True,
            'message': 'User payments retrieved successfully',
            'data': payments
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_user_payments_java_style: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': [str(e)]
        }), 500

@payment_java_bp.route('/<payment_id>/refund', methods=['POST'])
def refund_payment_java_style(payment_id):
    """
    Refund a payment (Java Spring Boot style)
    """
    try:
        if not payment_id:
            return jsonify({
                'success': False,
                'message': 'Payment ID is required',
                'errors': ['Payment ID cannot be empty']
            }), 400
        
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
            
            return jsonify({
                'success': True,
                'message': result['message'],
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'errors': result.get('errors', [])
            }), 400
            
    except Exception as e:
        logger.error(f"Error in refund_payment_java_style: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': [str(e)]
        }), 500

@payment_java_bp.route('/validate', methods=['POST'])
def validate_payment_method_java_style():
    """
    Validate payment method (Java Spring Boot style)
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided',
                'errors': ['Request body is required']
            }), 400
        
        # Convert Java-style field names
        validation_data = {
            'card_number': data.get('cardNumber'),
            'cvv': data.get('cvv'),
            'expiry_date': data.get('expiryDate')
        }
        
        # Validate payment method data
        is_valid, validation_errors = PaymentValidator.validate_payment_method(validation_data)
        
        if is_valid:
            return jsonify({
                'success': True,
                'message': 'Payment method is valid',
                'data': {'valid': True}
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Payment method validation failed',
                'errors': validation_errors
            }), 400
            
    except Exception as e:
        logger.error(f"Error in validate_payment_method_java_style: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'errors': [str(e)]
        }), 500

