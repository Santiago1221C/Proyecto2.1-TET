import logging
from datetime import datetime
from .mysql_connection import get_mysql_connection

logger = logging.getLogger(__name__)

class ReviewRepository:
    def __init__(self):
        logger.info("ReviewRepository now using MySQL")

    def create_review(self, review_data):
        """Create a new review"""
        conn = get_mysql_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO reviews (review_id, user_id, book_id, rating, text, status, helpful_count)
            VALUES (%s, %s, %s, %s, %s, 'active', 0)
        """
        cursor.execute(query, (
            review_data["review_id"],
            review_data["user_id"],
            review_data["book_id"],
            review_data["rating"],
            review_data.get("text", None)
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return review_data["review_id"]

    def get_review_by_id(self, review_id):
        """Retrieve a review by review_id"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reviews WHERE review_id=%s AND status='active'", (review_id,))
        review = cursor.fetchone()
        cursor.close()
        conn.close()
        return review

    def get_reviews_by_book(self, book_id, limit=50, skip=0):
        """Retrieve reviews for a specific book"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM reviews WHERE book_id=%s AND status='active' ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (book_id, limit, skip)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_reviews_by_user(self, user_id, limit=50, skip=0):
        """Retrieve reviews made by a specific user"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM reviews WHERE user_id=%s AND status='active' ORDER BY created_at DESC LIMIT %s OFFSET %s",
            (user_id, limit, skip)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_user_review_for_book(self, user_id, book_id):
        """Check if user has reviewed a specific book"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM reviews WHERE user_id=%s AND book_id=%s AND status='active'",
            (user_id, book_id)
        )
        review = cursor.fetchone()
        cursor.close()
        conn.close()
        return review

    def update_review(self, review_id, update_data):
        """Update review fields"""
        conn = get_mysql_connection()
        cursor = conn.cursor()

        set_clauses = ", ".join([f"{field}=%s" for field in update_data.keys()])
        query = f"""
            UPDATE reviews
            SET {set_clauses}, updated_at=%s
            WHERE review_id=%s
        """
        values = list(update_data.values()) + [datetime.utcnow(), review_id]

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def delete_review(self, review_id):
        """Soft delete review"""
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reviews SET status='deleted', updated_at=%s WHERE review_id=%s",
            (datetime.utcnow(), review_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def increment_helpful_count(self, review_id):
        """Increment helpful review counter"""
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE reviews SET helpful_count = helpful_count + 1, updated_at=%s WHERE review_id=%s",
            (datetime.utcnow(), review_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_book_rating_stats(self, book_id):
        """Calculate rating statistics for a book"""
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                AVG(rating) AS average_rating,
                COUNT(*) AS total_reviews
            FROM reviews
            WHERE book_id=%s AND status='active'
            """,
            (book_id,)
        )
        stats = cursor.fetchone()
        cursor.close()
        conn.close()

        return {
            "book_id": book_id,
            "average_rating": round(stats["average_rating"], 2) if stats["average_rating"] else 0,
            "total_reviews": stats["total_reviews"]
        }