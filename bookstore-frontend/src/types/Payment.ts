export interface PaymentRedirectResponse {
    redirectUrl: string;
    orderId: number;
}

export interface PaymentDetails {
    cardNumber: string;
    expiryDate: string;
    cvc: string;
    cardHolderName: string;
}

export interface InitiatePaymentData {
    orderId: number;
    amount: number;
    currency: 'USD' | 'EUR' | string;
    successUrl: string;
    cancelUrl: string;
}