from datetime import datetime
import uuid

class Review:
    def __init__(self, book_id, user_id, rating, title, comment, 
                 verified_purchase=False, review_id=None):
        self.review_id = review_id or str(uuid.uuid4())
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.title = title
        self.comment = comment
        self.verified_purchase = verified_purchase
        self.helpful_count = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.status = 'active'  # active, flagged, deleted
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'review_id': self.review_id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'verified_purchase': self.verified_purchase,
            'helpful_count': self.helpful_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data):
        """Create review from dictionary"""
        review = Review(
            book_id=data.get('book_id'),
            user_id=data.get('user_id'),
            rating=data.get('rating'),
            title=data.get('title'),
            comment=data.get('comment'),
            verified_purchase=data.get('verified_purchase', False),
            review_id=data.get('review_id')
        )
        
        if 'helpful_count' in data:
            review.helpful_count = data['helpful_count']
        if 'status' in data:
            review.status = data['status']
        if 'created_at' in data:
            review.created_at = data['created_at']
        if 'updated_at' in data:
            review.updated_at = data['updated_at']
        
        return review
    
    def validate(self):
        """Validate review data"""
        errors = []
        
        if not self.book_id:
            errors.append("Book ID is required")
        if not self.user_id:
            errors.append("User ID is required")
        if not self.rating or self.rating < 1 or self.rating > 5:
            errors.append("Rating must be between 1 and 5")
        if not self.title or len(self.title.strip()) == 0:
            errors.append("Title is required")
        if not self.comment or len(self.comment.strip()) == 0:
            errors.append("Comment is required")
        if len(self.title) > 200:
            errors.append("Title must be 200 characters or less")
        if len(self.comment) > 2000:
            errors.append("Comment must be 2000 characters or less")
        
        return len(errors) == 0, errors