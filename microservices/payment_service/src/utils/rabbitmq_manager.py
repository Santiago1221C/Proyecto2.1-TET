"""
RabbitMQ Connection Manager for Payment Service
Centralized RabbitMQ connection handling with retry logic and error handling
"""
import pika
import json
import logging
import time
from typing import Optional, Callable, Dict, Any
from contextlib import contextmanager
from .constants import PaymentConstants, LogMessages, ErrorMessages

logger = logging.getLogger(__name__)

class RabbitMQConnectionError(Exception):
    """Custom exception for RabbitMQ connection errors"""
    pass

class RabbitMQManager:
    """RabbitMQ connection manager with retry logic"""
    
    def __init__(self, config):
        """
        Initialize RabbitMQ manager
        
        Args:
            config: Configuration object with RabbitMQ settings
        """
        self.config = config
        self.connection = None
        self.channel = None
        self._connection_params = None
        self._setup_connection_params()
    
    def _setup_connection_params(self):
        """Setup connection parameters"""
        credentials = pika.PlainCredentials(
            self.config.RABBITMQ_USER,
            self.config.RABBITMQ_PASS
        )
        
        self._connection_params = pika.ConnectionParameters(
            host=self.config.RABBITMQ_HOST,
            port=self.config.RABBITMQ_PORT,
            virtual_host=self.config.RABBITMQ_VHOST,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
            connection_attempts=3,
            retry_delay=2
        )
    
    def connect(self, max_retries: int = PaymentConstants.MAX_RETRIES) -> bool:
        """
        Establish connection to RabbitMQ with retry logic
        
        Args:
            max_retries: Maximum number of connection attempts
            
        Returns:
            True if connection successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(self._connection_params)
                self.channel = self.connection.channel()
                
                # Setup exchanges and queues
                self._setup_exchanges()
                self._setup_queues()
                
                logger.info("RabbitMQ connection established successfully")
                return True
                
            except Exception as e:
                logger.warning(f"RabbitMQ connection attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(PaymentConstants.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"Failed to connect to RabbitMQ after {max_retries} attempts")
                    return False
        
        return False
    
    def _setup_exchanges(self):
        """Setup RabbitMQ exchanges"""
        exchanges = [
            (self.config.PAYMENT_EXCHANGE, 'topic'),
        ]
        
        for exchange_name, exchange_type in exchanges:
            self.channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=exchange_type,
                durable=True
            )
            logger.debug(f"Exchange '{exchange_name}' declared")
    
    def _setup_queues(self):
        """Setup RabbitMQ queues"""
        queues = [
            self.config.PAYMENT_QUEUE,
            self.config.PAYMENT_RESPONSE_QUEUE,
            self.config.ORDER_QUEUE
        ]
        
        for queue_name in queues:
            self.channel.queue_declare(queue=queue_name, durable=True)
            logger.debug(f"Queue '{queue_name}' declared")
    
    def is_connected(self) -> bool:
        """Check if connection is active"""
        return (self.connection is not None and 
                not self.connection.is_closed and 
                self.channel is not None and 
                not self.channel.is_closed)
    
    def reconnect(self) -> bool:
        """Reconnect to RabbitMQ"""
        self.close()
        return self.connect()
    
    def close(self):
        """Close RabbitMQ connection"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("RabbitMQ connection closed")
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {str(e)}")
        finally:
            self.connection = None
            self.channel = None
    
    @contextmanager
    def get_channel(self):
        """Context manager for getting a channel"""
        if not self.is_connected():
            if not self.reconnect():
                raise RabbitMQConnectionError("Failed to establish RabbitMQ connection")
        
        try:
            yield self.channel
        except Exception as e:
            logger.error(f"Error with RabbitMQ channel: {str(e)}")
            raise
    
    def publish_message(self, exchange: str, routing_key: str, message: Dict[str, Any], 
                       persistent: bool = True) -> bool:
        """
        Publish message to RabbitMQ
        
        Args:
            exchange: Exchange name
            routing_key: Routing key
            message: Message data
            persistent: Whether message should be persistent
            
        Returns:
            True if published successfully, False otherwise
        """
        try:
            with self.get_channel() as channel:
                properties = pika.BasicProperties(
                    delivery_mode=2 if persistent else 1,
                    timestamp=int(time.time()),
                    content_type='application/json'
                )
                
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=routing_key,
                    body=json.dumps(message),
                    properties=properties
                )
                
                logger.debug(f"Message published to {exchange} with routing key {routing_key}")
                return True
                
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            return False
    
    def consume_messages(self, queue: str, callback: Callable, auto_ack: bool = False):
        """
        Consume messages from a queue
        
        Args:
            queue: Queue name
            callback: Callback function for processing messages
            auto_ack: Whether to auto-acknowledge messages
        """
        try:
            with self.get_channel() as channel:
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(
                    queue=queue,
                    on_message_callback=callback,
                    auto_ack=auto_ack
                )
                
                logger.info(f"Started consuming messages from queue: {queue}")
                channel.start_consuming()
                
        except Exception as e:
            logger.error(f"Error consuming messages: {str(e)}")
            raise
    
    def stop_consuming(self):
        """Stop consuming messages"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.stop_consuming()
                logger.info("Stopped consuming messages")
        except Exception as e:
            logger.error(f"Error stopping message consumption: {str(e)}")
    
    def acknowledge_message(self, delivery_tag: int):
        """Acknowledge a message"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.basic_ack(delivery_tag=delivery_tag)
        except Exception as e:
            logger.error(f"Error acknowledging message: {str(e)}")
    
    def reject_message(self, delivery_tag: int, requeue: bool = False):
        """Reject a message"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.basic_nack(delivery_tag=delivery_tag, requeue=requeue)
        except Exception as e:
            logger.error(f"Error rejecting message: {str(e)}")
    
    def get_queue_info(self, queue: str) -> Optional[Dict[str, Any]]:
        """
        Get queue information
        
        Args:
            queue: Queue name
            
        Returns:
            Queue information dictionary or None if error
        """
        try:
            with self.get_channel() as channel:
                method = channel.queue_declare(queue=queue, passive=True)
                return {
                    'queue': queue,
                    'message_count': method.method.message_count,
                    'consumer_count': method.method.consumer_count
                }
        except Exception as e:
            logger.error(f"Error getting queue info: {str(e)}")
            return None

