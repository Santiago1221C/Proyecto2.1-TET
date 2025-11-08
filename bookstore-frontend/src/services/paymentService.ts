import axios from "axios";

// URL base para el microservicio de pagos
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8088";
const PAYMENT_SERVICE_URL = `${API_BASE_URL}/payment`; // Asume que la ruta es /api/payment


export const initiatePayment = async (orderId: number, amount: number): Promise<{ redirectUrl: string }> => {
  // Nota: En una aplicación real, probablemente también enviarías el token de autenticación del usuario.
  const response = await axios.post(`${PAYMENT_SERVICE_URL}/checkout`, {
    orderId,
    amount,
    currency: 'USD',
    // URLs de redirección para Stripe/Paypal, deben ser configuradas en el backend
    successUrl: window.location.origin + '/payment/success', 
    cancelUrl: window.location.origin + '/payment/cancel',
  });
  
  
  return response.data;
};