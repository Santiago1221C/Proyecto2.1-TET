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
        'service': 'review-service',
        'version': '1.0.0'
    }), 200

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness probe endpoint"""
    return jsonify({
        'status': 'ready',
        'service': 'review-service'
    }), 200