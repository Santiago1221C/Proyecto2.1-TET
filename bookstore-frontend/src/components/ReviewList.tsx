import { useState, useEffect } from "react";
import { getReviewsByBookId, createReview } from "../services/reviewService";
// 1. Importación explícita de los tipos
import type { Review, NewReviewData } from "../types/Review"; 

interface ReviewListProps {
    bookId: number;
}

const ReviewList = ({ bookId }: ReviewListProps) => {
    const userId = Number(localStorage.getItem("userId")) || 1; 
    
    // 2. USO CORRECTO: El estado se tipa explícitamente con Review[] (el tipo importado)
    const [reviews, setReviews] = useState<Review[]>([]); 
    
    const [loading, setLoading] = useState(true);
    const [newReview, setNewReview] = useState({ rating: 5, comment: '' });
    const [submitting, setSubmitting] = useState(false);

    const fetchReviews = async () => {
        setLoading(true);
        try {
            const data = await getReviewsByBookId(bookId);
            setReviews(data);
        } catch (err) {
            console.error("Error al cargar reseñas:", err);
            setReviews([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchReviews();
    }, [bookId]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newReview.comment.trim()) return alert("El comentario no puede estar vacío.");

        setSubmitting(true);
        try {
            const data: NewReviewData = {
                bookId,
                userId,
                rating: newReview.rating,
                comment: newReview.comment.trim(),
            };
            await createReview(data);
            setNewReview({ rating: 5, comment: '' }); 
            fetchReviews(); 
            alert('Reseña enviada exitosamente.');
        } catch (err) {
            console.error("Error al enviar reseña:", err);
            alert('Error al enviar la reseña.');
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) return <div className="mt-4">Cargando reseñas...</div>;

    return (
        <div className="mt-8">
            <h3 className="text-2xl font-semibold mb-4">⭐ Reseñas ({reviews.length})</h3>

            {/* Formulario de Reseña */}
            <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <h4 className="font-bold mb-3">Escribe tu opinión (Usuario ID: {userId})</h4>
                <form onSubmit={handleSubmit} className="space-y-3">
                    <div>
                        <label className="block text-sm font-medium">Calificación:</label>
                        <select value={newReview.rating} onChange={(e) => setNewReview({...newReview, rating: Number(e.target.value)})} className="mt-1 block w-full border rounded p-2">
                            {[5, 4, 3, 2, 1].map(n => <option key={n} value={n}>{n} Estrellas</option>)}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium">Comentario:</label>
                        <textarea rows={3} value={newReview.comment} onChange={(e) => setNewReview({...newReview, comment: e.target.value})} className="mt-1 block w-full border rounded p-2" required></textarea>
                    </div>
                    <button type="submit" disabled={submitting} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400">
                        {submitting ? 'Enviando...' : 'Enviar Reseña'}
                    </button>
                </form>
            </div>

            {/* Lista de Reseñas */}
            {reviews.length > 0 ? (
                <div className="space-y-4">
                    {reviews.map((review) => (
                        <div key={review.id} className="border p-3 rounded-lg bg-white">
                            <div className="flex justify-between items-center">
                                {/* Maneja el caso opcional: si userName es undefined, muestra el ID */}
                                <p className="font-semibold">{review.userName || `Usuario ${review.userId}`}</p> 
                                <p className="text-yellow-600">{'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}</p>
                            </div>
                            <p className="mt-1 text-gray-700">{review.comment}</p>
                        </div>
                    ))}
                </div>
            ) : (
                <p>Sé el primero en dejar una reseña para el libro {bookId}.</p>
            )}
        </div>
    );
};

export default ReviewList;