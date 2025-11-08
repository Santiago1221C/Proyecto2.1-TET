"""
Payment Service Business Logic
Simulates payment gateway processing with improved error handling and validation
"""
import time
import random
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from repository.payment_repository import PaymentRepository
from config.config import Config
from utils.constants import PaymentStatus, PaymentMethod, Currency, PaymentConstants, ErrorMessages, SuccessMessages
from utils.validators import PaymentValidator, ValidationError
from utils.api_response import ResponseBuilder, ErrorHandler
from utils.resilience_decorators import resilient_database_operation, resilient_payment_gateway, timeout

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self):
        """Initialize payment service"""
        self.repository = PaymentRepository()
        self.config = Config()
    
    @resilient_payment_gateway("simulated_gateway")
    @timeout(30)  # 30 second timeout for payment processing
    def process_payment(self, payment_data: Dict) -> Dict:
        """
        Process a payment request with improved validation and error handling
        
        Args:
            payment_data: Dictionary containing payment information
                - order_id: Order identifier
                - user_id: User identifier
                - amount: Payment amount
                - currency: Currency code (default: USD)
                - payment_method: Payment method (credit_card, debit_card, etc.)
        
        Returns:
            Dictionary with payment result
        """
        payment_id = None
        try:
            # Generate payment ID
            payment_id = str(uuid.uuid4())
            
            # Validate payment data
            is_valid, validation_errors = PaymentValidator.validate_payment_request(payment_data)
            if not is_valid:
                logger.warning(f"Payment validation failed: {validation_errors}")
                return {
                    'payment_id': payment_id,
                    'status': PaymentStatus.FAILED.value,
                    'message': ErrorMessages.VALIDATION_ERROR,
                    'errors': validation_errors,
                    'timestamp': datetime.utcnow().isoformat()
                }
            
            # Extract and validate payment data
            order_id = payment_data.get('order_id')
            user_id = payment_data.get('user_id')
            amount = float(payment_data.get('amount', 0))
            currency = payment_data.get('currency', Currency.USD.value)
            payment_method = payment_data.get('payment_method', PaymentMethod.CREDIT_CARD.value)
            
            # Check amount limits
            if amount < PaymentConstants.MIN_AMOUNT or amount > PaymentConstants.MAX_AMOUNT:
                return {
                    'payment_id': payment_id,
                    'status': PaymentStatus.FAILED.value,
                    'message': ErrorMessages.INVALID_AMOUNT,
                    'timestamp': datetime.utcnow().isoformat()
                }
            
            # Simulate payment processing time
            time.sleep(self.config.PAYMENT_PROCESSING_TIME)
            
            # Simulate payment gateway response
            success = random.random() < self.config.PAYMENT_SUCCESS_RATE
            
            if success:
                status = PaymentStatus.COMPLETED.value
                message = SuccessMessages.PAYMENT_PROCESSED
                transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
            else:
                status = PaymentStatus.FAILED.value
                message = ErrorMessages.PAYMENT_DECLINED
                transaction_id = None
            
            # Create payment record
            payment_record = {
                'payment_id': payment_id,
                'order_id': order_id,
                'user_id': user_id,
                'amount': amount,
                'currency': currency,
                'payment_method': payment_method,
                'status': status,
                'transaction_id': transaction_id,
                'message': message,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            
            # Save to database
            self.repository.create_payment(payment_record)
            
            logger.info(f"Payment {payment_id} processed with status: {status}")
            
            return {
                'payment_id': payment_id,
                'transaction_id': transaction_id,
                'status': status,
                'message': message,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except ValidationError as e:
            logger.warning(f"Payment validation error: {str(e)}")
            return {
                'payment_id': payment_id,
                'status': PaymentStatus.FAILED.value,
                'message': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            return {
                'payment_id': payment_id,
                'status': PaymentStatus.FAILED.value,
                'message': ErrorMessages.INTERNAL_ERROR,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    @resilient_database_operation("get_payment_status")
    def get_payment_status(self, payment_id: str) -> Optional[Dict]:
        """Get payment status by ID with improved error handling"""
        try:
            if not payment_id or not isinstance(payment_id, str):
                logger.warning("Invalid payment ID provided")
                return None
                
            payment = self.repository.get_payment_by_id(payment_id)
            if payment:
                return {
                    'payment_id': payment['payment_id'],
                    'status': payment['status'],
                    'amount': payment['amount'],
                    'currency': payment['currency'],
                    'transaction_id': payment.get('transaction_id'),
                    'message': payment['message'],
                    'created_at': payment['created_at'].isoformat() if payment.get('created_at') else None
                }
            return None
        except Exception as e:
            logger.error(f"Error retrieving payment status: {str(e)}")
            return None
    
    @resilient_database_operation("get_user_payments")
    def get_user_payments(self, user_id: str) -> List[Dict]:
        """Get all payments for a user with improved error handling"""
        try:
            if not user_id or not isinstance(user_id, str):
                logger.warning("Invalid user ID provided")
                return []
                
            payments = self.repository.get_payments_by_user(user_id)
            return [{
                'payment_id': p['payment_id'],
                'order_id': p['order_id'],
                'amount': p['amount'],
                'currency': p['currency'],
                'status': p['status'],
                'created_at': p['created_at'].isoformat() if p.get('created_at') else None
            } for p in payments]
        except Exception as e:
            logger.error(f"Error retrieving user payments: {str(e)}")
            return []
    
    @resilient_payment_gateway("refund_gateway")
    @timeout(60)  # 60 second timeout for refund processing
    def refund_payment(self, payment_id: str) -> Dict:
        """Refund a payment with improved validation and error handling"""
        try:
            if not payment_id or not isinstance(payment_id, str):
                return {
                    'success': False,
                    'message': ErrorMessages.PAYMENT_NOT_FOUND,
                    'payment_id': payment_id
                }
            
            payment = self.repository.get_payment_by_id(payment_id)
            
            if not payment:
                return {
                    'success': False,
                    'message': ErrorMessages.PAYMENT_NOT_FOUND,
                    'payment_id': payment_id
                }
            
            if payment['status'] != PaymentStatus.COMPLETED.value:
                return {
                    'success': False,
                    'message': ErrorMessages.PAYMENT_CANNOT_BE_REFUNDED,
                    'payment_id': payment_id,
                    'current_status': payment['status']
                }
            
            # Simulate refund processing
            time.sleep(1)
            
            # Update payment status
            self.repository.update_payment_status(payment_id, PaymentStatus.REFUNDED.value)
            
            logger.info(f"Payment {payment_id} refunded successfully")
            
            return {
                'success': True,
                'message': SuccessMessages.PAYMENT_REFUNDED,
                'payment_id': payment_id,
                'refunded_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error refunding payment: {str(e)}")
            return {
                'success': False,
                'message': ErrorMessages.INTERNAL_ERROR,
                'payment_id': payment_id
            }

