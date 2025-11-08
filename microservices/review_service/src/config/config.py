import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('PORT', 5002))
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'review-service')
    
    # RabbitMQ Configuration
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'bookstore')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'santi1234')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    
    # RabbitMQ Queues and Exchanges
    REVIEW_QUEUE = 'review_notifications'
    REVIEW_EXCHANGE = 'review_exchange'
    PAYMENT_EXCHANGE = 'payment_exchange'
    
    # Security
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'