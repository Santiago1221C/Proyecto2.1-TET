// Estructura de datos enviada al backend para iniciar el checkout
export interface PaymentUser {
  fullName: string;
  email: string;
  contactPhone?: string;
  dniNumber?: string;
  dniType?: string;
  shippingAddress?: any;
}

export interface PaymentCard {
  number: string;
  securityCode: string;
  expirationDate: string;
  cardHolderName: string;
  paymentMethod?: string;
}

export interface PaymentPse {
  bankCode: string;
  userType: string;
}

export interface PaymentOrder {
  orderId: string;
  amount: number;
  responseUrl?: string;
  notifyUrl?: string;
}

export interface PaymentCheckoutRequest {
  paymentMethod: "CC" | "PSE";
  order: PaymentOrder;
  user: PaymentUser;
  card?: PaymentCard;
  pse?: PaymentPse;
  deviceSessionId?: string;
  cookie?: string;
}

export interface PaymentCheckoutResponse {
  message?: string;
  status?: string;
  redirectionUrl?: string;
  details?: any;
  error?: string;
  payuResponseDetails?: any;
}
