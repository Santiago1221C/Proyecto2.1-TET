import os
from dotenv import load_dotenv
import pika
import json
import logging
from config.config import Config

logger = logging.getLogger(__name__)

class ReviewProducer:
    def __init__(self):
        """Initialize RabbitMQ producer"""
        self.config = Config()
        
    def get_connection(self):
        """Create a new connection to RabbitMQ"""
        credentials = pika.PlainCredentials(
            self.config.RABBITMQ_USER,
            self.config.RABBITMQ_PASS
        )
        parameters = pika.ConnectionParameters(
            host=self.config.RABBITMQ_HOST,
            port=self.config.RABBITMQ_PORT,
            virtual_host=self.config.RABBITMQ_VHOST,
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)
    
    def publish_review_event(self, event_type, review_data):
        """
        Publish review events to RabbitMQ
        
        Args:
            event_type: Type of event (created, updated, deleted)
            review_data: Review data dictionary
        """
        try:
            connection = self.get_connection()
            channel = connection.channel()
            
            # Declare exchange
            channel.exchange_declare(
                exchange=self.config.REVIEW_EXCHANGE,
                exchange_type='topic',
                durable=True
            )
            
            message = {
                'event_type': event_type,
                'data': review_data,
                'service': 'review-service'
            }
            
            routing_key = f'review.{event_type}'
            
            channel.basic_publish(
                exchange=self.config.REVIEW_EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                    content_type='application/json'
                )
            )
            
            logger.info(f"Published review event: {event_type} for review {review_data.get('review_id')}")
            connection.close()
            return True
            
        except Exception as e:
            logger.error(f"Error publishing review event: {str(e)}")
            return False