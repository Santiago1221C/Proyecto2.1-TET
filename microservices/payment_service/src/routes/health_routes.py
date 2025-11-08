"""
Health Check Routes
"""
from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
@health_bp.route('/live', methods=['GET'])
def health_check():
    """Liveness probe endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'payment-service',
        'version': '1.0.0'
    }), 200

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness probe endpoint"""
    # Could add checks for DB connection, RabbitMQ, etc.
    return jsonify({
        'status': 'ready',
        'service': 'payment-service'
    }), 200

