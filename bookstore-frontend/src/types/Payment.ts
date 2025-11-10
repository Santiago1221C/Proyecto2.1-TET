// Estructura de datos enviada al backend para iniciar el checkout
export interface InitiatePaymentData {
    orderId: number;
    amount: number;
    currency: 'USD' | 'EUR' | string;
    successUrl: string; // URL de redirección en caso de éxito
    cancelUrl: string;  // URL de redirección en caso de cancelación o fallo
}
export interface PaymentResponse {
    message?: string;
    error?: string;
    details?: string;
    redirectUrl: string; // La URL a donde el frontend debe redirigir
    transactionId?: string;
}

// Interfaz para la captura de tarjeta (no usada en el frontend actual, pero útil)
export interface PaymentDetails {
    cardNumber: string;
    expiryDate: string;
    cvc: string;
    cardHolderName: string;
}