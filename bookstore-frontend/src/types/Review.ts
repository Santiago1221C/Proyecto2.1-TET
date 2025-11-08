export interface Review {
    id: number;
    bookId: number;
    userId: number;
    userName?: string; // El backend puede incluir el nombre del usuario
    rating: number; // 1 a 5 estrellas
    comment: string;
    createdAt: string; // Fecha y hora de la reseña
}

export interface NewReviewData {
    bookId: number;
    userId: number;
    rating: number;
    comment: string;
}