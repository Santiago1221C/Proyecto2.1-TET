"""
RabbitMQ Producer for Payment Service
Sends payment notifications and events to other services with improved error handling
"""
import json
import logging
from typing import Dict, Any, Optional
from config.config import Config
from utils.rabbitmq_manager import RabbitMQManager
from utils.constants import EventType, LogMessages, ErrorMessages
from utils.resilience_decorators import resilient_message_queue, timeout

logger = logging.getLogger(__name__)

class PaymentProducer:
    """Enhanced RabbitMQ producer with connection management and retry logic"""
    
    def __init__(self):
        """Initialize RabbitMQ producer with connection manager"""
        self.config = Config()
        self.rabbitmq_manager = RabbitMQManager(self.config)
        self._ensure_connection()
    
    def _ensure_connection(self):
        """Ensure RabbitMQ connection is established"""
        if not self.rabbitmq_manager.is_connected():
            if not self.rabbitmq_manager.connect():
                logger.error("Failed to establish RabbitMQ connection")
                raise ConnectionError("Cannot connect to RabbitMQ")
    
    @resilient_message_queue("payment_events")
    @timeout(10)  # 10 second timeout for message publishing
    def publish_payment_event(self, event_type: str, payment_data: Dict[str, Any]) -> bool:
        """
        Publish payment events to RabbitMQ with improved error handling
        
        Args:
            event_type: Type of payment event
            payment_data: Payment data to publish
            
        Returns:
            True if published successfully, False otherwise
        """
        try:
            # Ensure connection is active
            if not self.rabbitmq_manager.is_connected():
                if not self.rabbitmq_manager.reconnect():
                    logger.error("Failed to reconnect to RabbitMQ")
                    return False
            
            # Prepare message
            message = {
                'event_type': event_type,
                'service': 'payment-service',
                'timestamp': payment_data.get('timestamp'),
                'data': payment_data
            }
            
            # Determine routing key based on event type
            routing_key = self._get_routing_key(event_type)
            
            # Publish message
            success = self.rabbitmq_manager.publish_message(
                exchange=self.config.PAYMENT_EXCHANGE,
                routing_key=routing_key,
                message=message,
                persistent=True
            )
            
            if success:
                logger.info(f"Published payment event: {event_type}")
            else:
                logger.error(f"Failed to publish payment event: {event_type}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error publishing payment event: {str(e)}")
            return False
    
    def _get_routing_key(self, event_type: str) -> str:
        """
        Get routing key for event type
        
        Args:
            event_type: Type of event
            
        Returns:
            Routing key string
        """
        routing_keys = {
            'completed': EventType.PAYMENT_COMPLETED.value,
            'failed': EventType.PAYMENT_FAILED.value,
            'refunded': EventType.PAYMENT_REFUNDED.value,
            'request': EventType.PAYMENT_REQUEST.value,
            'response': EventType.PAYMENT_RESPONSE.value
        }
        
        return routing_keys.get(event_type, f'payment.{event_type}')
    
    @resilient_message_queue("payment_requests")
    @timeout(10)
    def publish_payment_request(self, order_data: Dict[str, Any]) -> bool:
        """
        Publish payment request event
        
        Args:
            order_data: Order data for payment processing
            
        Returns:
            True if published successfully, False otherwise
        """
        return self.publish_payment_event('request', order_data)
    
    @resilient_message_queue("payment_responses")
    @timeout(10)
    def publish_payment_response(self, payment_result: Dict[str, Any]) -> bool:
        """
        Publish payment response event
        
        Args:
            payment_result: Payment processing result
            
        Returns:
            True if published successfully, False otherwise
        """
        return self.publish_payment_event('response', payment_result)
    
    def close(self):
        """Close RabbitMQ connection"""
        self.rabbitmq_manager.close()

