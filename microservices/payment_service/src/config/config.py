import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('PORT', 5000))
    SERVICE_NAME = os.getenv('SERVICE_NAME', 'payment-service')
    
    # RabbitMQ Configuration
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    
    # RabbitMQ Queues and Exchanges
    PAYMENT_QUEUE = 'payment_requests'
    PAYMENT_RESPONSE_QUEUE = 'payment_responses'
    ORDER_QUEUE = 'order_events'
    PAYMENT_EXCHANGE = 'payment_exchange'
    
    # MongoDB Configuration
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB = os.getenv('MONGO_DB', 'payment_db')
    
    # Security
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    
    # Payment Gateway Simulation
    PAYMENT_SUCCESS_RATE = 0.85  # 85% success rate for simulation
    PAYMENT_PROCESSING_TIME = 2  # seconds

