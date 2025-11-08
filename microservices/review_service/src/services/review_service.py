import logging
from datetime import datetime
from models.review import Review
from repository.review_repository import ReviewRepository
from events.review_producer import ReviewProducer

logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self):
        """Initialize review service"""
        self.repository = ReviewRepository()
        self.event_producer = ReviewProducer()
    
    def create_review(self, review_data):
        """Create a new review"""
        try:
            # Create review object
            review = Review(
                book_id=review_data.get('book_id'),
                user_id=review_data.get('user_id'),
                rating=review_data.get('rating'),
                title=review_data.get('title'),
                comment=review_data.get('comment'),
                verified_purchase=review_data.get('verified_purchase', False)
            )
            
            # Validate review
            is_valid, errors = review.validate()
            if not is_valid:
                return {
                    'success': False,
                    'errors': errors
                }
            
            # Check if user already reviewed this book
            existing_review = self.repository.get_user_review_for_book(
                review.user_id, review.book_id
            )
            if existing_review:
                return {
                    'success': False,
                    'errors': ['You have already reviewed this book']
                }
            
            # Save review
            self.repository.create_review(review.to_dict())
            
            # Publish event to RabbitMQ
            self.event_producer.publish_review_event('created', review.to_dict())
            
            logger.info(f"Review {review.review_id} created successfully")
            
            return {
                'success': True,
                'review': review.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error creating review: {str(e)}")
            return {
                'success': False,
                'errors': [str(e)]
            }
    
    def get_review(self, review_id):
        """Get review by ID"""
        review = self.repository.get_review_by_id(review_id)
        return review
    
    def get_book_reviews(self, book_id, page=1, limit=20):
        """Get all reviews for a book"""
        skip = (page - 1) * limit
        reviews = self.repository.get_reviews_by_book(book_id, limit, skip)
        
        # Clean up MongoDB _id field
        for review in reviews:
            if '_id' in review:
                del review['_id']
            if 'created_at' in review and isinstance(review['created_at'], datetime):
                review['created_at'] = review['created_at'].isoformat()
            if 'updated_at' in review and isinstance(review['updated_at'], datetime):
                review['updated_at'] = review['updated_at'].isoformat()
        
        return reviews
    
    def get_user_reviews(self, user_id, page=1, limit=20):
        """Get all reviews by a user"""
        skip = (page - 1) * limit
        reviews = self.repository.get_reviews_by_user(user_id, limit, skip)
        
        # Clean up MongoDB _id field
        for review in reviews:
            if '_id' in review:
                del review['_id']
            if 'created_at' in review and isinstance(review['created_at'], datetime):
                review['created_at'] = review['created_at'].isoformat()
            if 'updated_at' in review and isinstance(review['updated_at'], datetime):
                review['updated_at'] = review['updated_at'].isoformat()
        
        return reviews
    
    def update_review(self, review_id, user_id, update_data):
        """Update a review"""
        try:
            # Get existing review
            review = self.repository.get_review_by_id(review_id)
            if not review:
                return {
                    'success': False,
                    'error': 'Review not found'
                }
            
            # Check if user owns the review
            if review['user_id'] != user_id:
                return {
                    'success': False,
                    'error': 'You can only update your own reviews'
                }
            
            # Prepare update data
            allowed_fields = ['rating', 'title', 'comment']
            filtered_update = {
                k: v for k, v in update_data.items() 
                if k in allowed_fields
            }
            
            if not filtered_update:
                return {
                    'success': False,
                    'error': 'No valid fields to update'
                }
            
            # Update review
            success = self.repository.update_review(review_id, filtered_update)
            
            if success:
                # Publish update event
                self.event_producer.publish_review_event('updated', {
                    'review_id': review_id,
                    'book_id': review['book_id']
                })
                
                logger.info(f"Review {review_id} updated successfully")
                return {
                    'success': True,
                    'message': 'Review updated successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to update review'
                }
                
        except Exception as e:
            logger.error(f"Error updating review: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_review(self, review_id, user_id):
        """Delete a review"""
        try:
            # Get existing review
            review = self.repository.get_review_by_id(review_id)
            if not review:
                return {
                    'success': False,
                    'error': 'Review not found'
                }
            
            # Check if user owns the review
            if review['user_id'] != user_id:
                return {
                    'success': False,
                    'error': 'You can only delete your own reviews'
                }
            
            # Delete review (soft delete)
            success = self.repository.delete_review(review_id)
            
            if success:
                # Publish delete event
                self.event_producer.publish_review_event('deleted', {
                    'review_id': review_id,
                    'book_id': review['book_id']
                })
                
                logger.info(f"Review {review_id} deleted successfully")
                return {
                    'success': True,
                    'message': 'Review deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to delete review'
                }
                
        except Exception as e:
            logger.error(f"Error deleting review: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def mark_review_helpful(self, review_id):
        """Mark a review as helpful"""
        try:
            success = self.repository.increment_helpful_count(review_id)
            if success:
                return {
                    'success': True,
                    'message': 'Review marked as helpful'
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to mark review as helpful'
                }
        except Exception as e:
            logger.error(f"Error marking review as helpful: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_book_rating_stats(self, book_id):
        """Get rating statistics for a book"""
        return self.repository.get_book_rating_stats(book_id)