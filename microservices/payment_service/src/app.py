"""
Payment Service - Microservice for handling payment processing
Author: Bookstore Microservices Architecture
Description: Simulates a payment gateway with RabbitMQ integration
"""

from flask import Flask, jsonify
from flask_cors import CORS
from config.config import Config
from routes.payment_routes import payment_bp
from routes.payment_routes_java import payment_java_bp
from routes.health_routes import health_bp
from events.payment_consumer import PaymentConsumer
from events.payment_producer import PaymentProducer
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    app.register_blueprint(payment_java_bp, url_prefix='/api/payments/java')
    
    # Initialize RabbitMQ consumer in a separate thread
    def start_consumer():
        try:
            consumer = PaymentConsumer()
            logger.info("Starting RabbitMQ consumer...")
            consumer.start_consuming()
        except Exception as e:
            logger.error(f"Error starting consumer: {str(e)}")
    
    # Start consumer thread
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    
    logger.info(f"Payment Service started on port {app.config['PORT']}")
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )

