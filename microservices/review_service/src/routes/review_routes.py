from flask import Blueprint, request, jsonify
from services.review_service import ReviewService
import logging

logger = logging.getLogger(__name__)
review_bp = Blueprint('review', __name__)
review_service = ReviewService()

@review_bp.route('/', methods=['POST'])
def create_review():
    """
    Create a new review
    Request body:
    {
        "book_id": "string",
        "user_id": "string",
        "rating": int (1-5),
        "title": "string",
        "comment": "string",
        "verified_purchase": boolean
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        result = review_service.create_review(data)
        
        if result['success']:
            return jsonify(result['review']), 201
        else:
            return jsonify({'errors': result['errors']}), 400
        
    except Exception as e:
        logger.error(f"Error in create_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    """Get review by ID"""
    try:
        review = review_service.get_review(review_id)
        
        if review:
            # Clean up MongoDB _id
            if '_id' in review:
                del review['_id']
            # Convert datetime to string
            if 'created_at' in review:
                review['created_at'] = review['created_at'].isoformat() if hasattr(review['created_at'], 'isoformat') else review['created_at']
            if 'updated_at' in review:
                review['updated_at'] = review['updated_at'].isoformat() if hasattr(review['updated_at'], 'isoformat') else review['updated_at']
            
            return jsonify(review), 200
        else:
            return jsonify({'error': 'Review not found'}), 404
        
    except Exception as e:
        logger.error(f"Error in get_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/book/<book_id>', methods=['GET'])
def get_book_reviews(book_id):
    """Get all reviews for a book"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        reviews = review_service.get_book_reviews(book_id, page, limit)
        
        return jsonify({
            'book_id': book_id,
            'reviews': reviews,
            'page': page,
            'limit': limit,
            'count': len(reviews)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_book_reviews: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/user/<user_id>', methods=['GET'])
def get_user_reviews(user_id):
    """Get all reviews by a user"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        reviews = review_service.get_user_reviews(user_id, page, limit)
        
        return jsonify({
            'user_id': user_id,
            'reviews': reviews,
            'page': page,
            'limit': limit,
            'count': len(reviews)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_user_reviews: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update a review
    Request body:
    {
        "user_id": "string",
        "rating": int (optional),
        "title": "string" (optional),
        "comment": "string" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id is required'}), 400
        
        user_id = data.pop('user_id')
        result = review_service.update_review(review_id, user_id, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error in update_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review
    Query param: user_id
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        result = review_service.delete_review(review_id, user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error in delete_review: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/<review_id>/helpful', methods=['POST'])
def mark_helpful(review_id):
    """Mark a review as helpful"""
    try:
        result = review_service.mark_review_helpful(review_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        logger.error(f"Error in mark_helpful: {str(e)}")
        return jsonify({'error': str(e)}), 500

@review_bp.route('/book/<book_id>/stats', methods=['GET'])
def get_book_stats(book_id):
    """Get rating statistics for a book"""
    try:
        stats = review_service.get_book_rating_stats(book_id)
        
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({'error': 'Could not retrieve stats'}), 500
        
    except Exception as e:
        logger.error(f"Error in get_book_stats: {str(e)}")
        return jsonify({'error': str(e)}), 500