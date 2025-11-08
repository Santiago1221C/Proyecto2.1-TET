import axios from "axios";
import type { UserProfile, UserUpdateData } from "../types/User"; 

// URL base para el microservicio de usuarios
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8088";
const USER_SERVICE_URL = `${API_BASE_URL}/user`; 

// Obtener detalles del perfil de usuario
export const getUserProfile = async (userId: number): Promise<UserProfile> => {
  // En producción, probablemente usarías un token y no el userId directo en la URL
  const response = await axios.get(`${USER_SERVICE_URL}/profile/${userId}`); 
  return response.data;
};

// Actualizar perfil de usuario
export const updateProfile = async (userId: number, data: UserUpdateData): Promise<UserProfile> => {
  const response = await axios.put(`${USER_SERVICE_URL}/profile/${userId}`, data);
  return response.data;
};