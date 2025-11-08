"""
Payment Repository - Data Access Layer
Handles MongoDB operations for payments
"""
from pymongo import MongoClient
from datetime import datetime
import logging
from config.config import Config

logger = logging.getLogger(__name__)

class PaymentRepository:
    def __init__(self):
        """Initialize MongoDB connection"""
        self.config = Config()
        try:
            self.client = MongoClient(self.config.MONGO_URI)
            self.db = self.client[self.config.MONGO_DB]
            self.payments = self.db.payments
            
            # Create indexes
            self.payments.create_index('payment_id', unique=True)
            self.payments.create_index('order_id')
            self.payments.create_index('user_id')
            self.payments.create_index('status')
            
            logger.info("MongoDB connection established")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {str(e)}")
            raise
    
    def create_payment(self, payment_data):
        """Create a new payment record"""
        try:
            result = self.payments.insert_one(payment_data)
            logger.info(f"Payment created with ID: {payment_data['payment_id']}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}")
            raise
    
    def get_payment_by_id(self, payment_id):
        """Get payment by payment_id"""
        try:
            return self.payments.find_one({'payment_id': payment_id})
        except Exception as e:
            logger.error(f"Error getting payment: {str(e)}")
            return None
    
    def get_payments_by_user(self, user_id):
        """Get all payments for a user"""
        try:
            return list(self.payments.find({'user_id': user_id}).sort('created_at', -1))
        except Exception as e:
            logger.error(f"Error getting user payments: {str(e)}")
            return []
    
    def get_payments_by_order(self, order_id):
        """Get all payments for an order"""
        try:
            return list(self.payments.find({'order_id': order_id}))
        except Exception as e:
            logger.error(f"Error getting order payments: {str(e)}")
            return []
    
    def update_payment_status(self, payment_id, status):
        """Update payment status"""
        try:
            result = self.payments.update_one(
                {'payment_id': payment_id},
                {
                    '$set': {
                        'status': status,
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            logger.info(f"Payment {payment_id} status updated to {status}")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating payment status: {str(e)}")
            return False
    
    def get_all_payments(self, limit=100, skip=0):
        """Get all payments with pagination"""
        try:
            return list(
                self.payments.find()
                .sort('created_at', -1)
                .skip(skip)
                .limit(limit)
            )
        except Exception as e:
            logger.error(f"Error getting all payments: {str(e)}")
            return []

