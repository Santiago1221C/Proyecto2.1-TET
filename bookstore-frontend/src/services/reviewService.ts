import axios from "axios";
import type { Review, NewReviewData } from "../types/Review"; 

// URL base para el microservicio de reseñas
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8088";
const REVIEW_SERVICE_URL = `${API_BASE_URL}/review`; 

// Obtener todas las reseñas de un libro
export const getReviewsByBookId = async (bookId: number): Promise<Review[]> => {
  const response = await axios.get(`${REVIEW_SERVICE_URL}/book/${bookId}`);
  return response.data;
};

// Enviar una nueva reseña
export const createReview = async (data: NewReviewData): Promise<Review> => {
  const response = await axios.post(`${REVIEW_SERVICE_URL}`, data);
  return response.data;
};