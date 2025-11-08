import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8088/orders";

// Crear orden a partir del carrito del usuario
export const createOrder = async (userId: number) => {
    const response = await axios.post(`${API_BASE_URL}/${userId}`)
    return response.data;
};

// Obtener todas las órdenes del usuario
export const getAllOrdersByUserId = async (userId: number) => {
    const response = await axios.get(`${API_BASE_URL}/user/${userId}`);
    return response.data;
};