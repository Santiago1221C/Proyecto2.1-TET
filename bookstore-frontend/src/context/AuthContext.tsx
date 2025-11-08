import { createContext, useContext, useState, useEffect } from "react";
import type { ReactNode } from "react";
import axios from "axios";

interface AuthContextType {
    isAuthenticated: boolean;
    userId: number | null;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, password: string, username: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const API_URL = ""; // Hay que cambiarlo por la URL al servicio de usuarios

export const AuthProvider = ({ children }: { children: ReactNode}) => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [userId, setUserId] = useState<number | null>(null);

    // Cargar datos desde localStorage al inicializar
    useEffect(() => {
        const savedUserId = localStorage.getItem("userId")
        if (savedUserId) {
            setUserId(+savedUserId);
            setIsAuthenticated(true);
        }
    }, []);

    const login = async (email: string, password: string) => {
        const response = await axios.post(`${API_URL}/login`, { email, password });
        const data = response.data;

        setIsAuthenticated(true);
        setUserId(data.userId);
        localStorage.setItem("userId", `${data.userId}`);
    };

    const register = async (email: string, password: string, username: string) => {
        await axios.post(`${API_URL}/register`, { email, password, username});
    }

    const logout = () => {
        setIsAuthenticated(false);
        setUserId(null);
        localStorage.removeItem("userId");
    }

    return (
        <AuthContext.Provider value={{ isAuthenticated, userId, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context){
        throw new Error("useAuth debe utilizarse dentro de un AuthProvider.")
    }
    return context;
};