"""
RabbitMQ Consumer for Payment Service
Listens for payment requests from other services
"""
import pika
import json
import logging
from config.config import Config
from services.payment_service import PaymentService

logger = logging.getLogger(__name__)

class PaymentConsumer:
    def __init__(self):
        """Initialize RabbitMQ consumer"""
        self.config = Config()
        self.payment_service = PaymentService()
        self.connection = None
        self.channel = None
        
    def connect(self):
        """Establish connection to RabbitMQ"""
        credentials = pika.PlainCredentials(
            self.config.RABBITMQ_USER,
            self.config.RABBITMQ_PASS
        )
        parameters = pika.ConnectionParameters(
            host=self.config.RABBITMQ_HOST,
            port=self.config.RABBITMQ_PORT,
            virtual_host=self.config.RABBITMQ_VHOST,
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )
        
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        # Declare exchange
        self.channel.exchange_declare(
            exchange=self.config.PAYMENT_EXCHANGE,
            exchange_type='topic',
            durable=True
        )
        
        # Declare queues
        self.channel.queue_declare(queue=self.config.PAYMENT_QUEUE, durable=True)
        self.channel.queue_bind(
            exchange=self.config.PAYMENT_EXCHANGE,
            queue=self.config.PAYMENT_QUEUE,
            routing_key='payment.request'
        )
        
        logger.info("Connected to RabbitMQ successfully")
        
    def callback(self, ch, method, properties, body):
        """Process incoming payment requests"""
        try:
            payment_data = json.loads(body)
            logger.info(f"Received payment request: {payment_data}")
            
            # Process payment
            result = self.payment_service.process_payment(payment_data)
            
            # Send response back
            response_message = {
                'order_id': payment_data.get('order_id'),
                'payment_id': result.get('payment_id'),
                'status': result.get('status'),
                'message': result.get('message'),
                'timestamp': result.get('timestamp')
            }
            
            # Publish response
            self.channel.basic_publish(
                exchange=self.config.PAYMENT_EXCHANGE,
                routing_key='payment.response',
                body=json.dumps(response_message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    correlation_id=properties.correlation_id
                )
            )
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Payment processed successfully: {result}")
            
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        """Start consuming messages"""
        self.connect()
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.config.PAYMENT_QUEUE,
            on_message_callback=self.callback
        )
        
        logger.info("Waiting for payment requests...")
        self.channel.start_consuming()
    
    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed")

