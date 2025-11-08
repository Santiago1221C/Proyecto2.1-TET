import axios from "axios";
import type { Book } from "../types/Book";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8088").replace(/\/$/, "");
const API_BASE_URL = `${API_BASE}/catalog`;

export const getAllBooks = async (): Promise<Book[]> => {
  const response = await axios.get<Book[]>(`${API_BASE_URL}/books`);
  return response.data;
};

export const getBookById = async (bookId: number): Promise<Book> => {
  const response = await axios.get<Book>(`${API_BASE_URL}/books/${bookId}`);
  return response.data;
};

// (Opcionales si los necesitas)
export const createBook = async (book: Partial<Book>) => {
  const response = await axios.post<Book>(`${API_BASE_URL}/books`, book);
  return response.data;
};

export const updateBook = async (bookId: number, payload: Partial<Book>) => {
  const response = await axios.put<Book>(`${API_BASE_URL}/books/${bookId}`, payload);
  return response.data;
};

export const decreaseStock = async (bookId: number, quantity: number) => {
  // Si usas el endpoint REST del controlador que creaste:
  const response = await axios.put<string>(`${API_BASE_URL}/${bookId}/decreaseStock`, null, {
    params: { quantity },
  });
  return response.data;
};