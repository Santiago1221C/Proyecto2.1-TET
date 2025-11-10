import axios from "axios";
import type { InitiatePaymentData, PaymentResponse } from "../types/Payment"; 

// URL base para el microservicio de pagos
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8088";
const PAYMENT_SERVICE_URL = `${API_BASE_URL}/payment`; 

export const initiatePayment = async (orderId: number, amount: number): Promise<PaymentResponse> => {
  
    const requestData: InitiatePaymentData = {
        orderId,
        amount,
        currency: 'USD',
        successUrl: window.location.origin + '/payment/success', 
        cancelUrl: window.location.origin + '/payment/cancel',
    };

    try {

        const response = await axios.post<PaymentResponse>(`${PAYMENT_SERVICE_URL}/checkout`, requestData);
        
        return response.data;
        
    } catch (error) {

        if (axios.isAxiosError(error) && error.response) {
            
            if (error.response.data && error.response.data.redirectUrl) {
                return error.response.data as PaymentResponse; 
            }
            
            throw new Error(error.response.data.error || "Error de servicio de pagos desconocido.");
        }
        
        
        throw new Error("Error al comunicar con el Payment Service");
    }
};