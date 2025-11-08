import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8088/cart";

export const createCart = async (userId: number) => {
  const response = await axios.post(`${API_BASE_URL}/create/${userId}`);
  return response.data;
};

export const addItemToCart = async (userId: number, item: any) => {
  const response = await axios.post(`${API_BASE_URL}/${userId}/add`, item);
  return response.data;
};

export const getCartByUserId = async (userId: number) => {
  const response = await axios.get(`${API_BASE_URL}/${userId}`);
  return response.data;
};

export const removeItemFromCart = async (userId: number, bookId: number) => {
  const response = await axios.delete(`${API_BASE_URL}/${userId}/remove/${bookId}`);
  return response.data;
};

export const clearCart = async (userId: number) => {
  const response = await axios.delete(`${API_BASE_URL}/${userId}`);
  return response.data;
};

export const deleteCart = async (userId: number) => {
  const response = await axios.delete(`${API_BASE_URL}/${userId}/delete`);
  return response.data;
};