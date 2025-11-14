const RAW_API_BASE =
  (globalThis as any)?.REACT_APP_API_BASE ||
  (globalThis as any)?.process?.env?.REACT_APP_API_BASE ||
  (window as any)?.REACT_APP_API_BASE ||
  "";

export const API_BASE = RAW_API_BASE.startsWith("http")
  ? RAW_API_BASE.replace(/\/+$/, "")
  : `http://${RAW_API_BASE.replace(/\/+$/, "")}`;

export type CheckoutPayload = {
  paymentMethod: "CC" | "PSE";
  order: {
    orderId: string;
    amount: number;
    responseUrl?: string;
    notifyUrl?: string;
  };
  user: {
    fullName: string;
    email: string;
    contactPhone?: string;
    dniNumber?: string;
    dniType?: string;
    shippingAddress?: any;
  };
  card?: {
    number: string;
    securityCode: string;
    expirationDate: string;
    cardHolderName: string;
    paymentMethod?: string;
  };
  pse?: {
    bankCode: string;
    userType: string;
  };
  deviceSessionId?: string;
  cookie?: string;
};

export async function getPseBanks(): Promise<any> {
  const url = `${API_BASE}/banks/pse`;
  const res = await fetch(url, { method: "GET" });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function checkout(payload: CheckoutPayload): Promise<any> {
  const url = `${API_BASE}/checkout`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const text = await res.text();
  const json = text ? JSON.parse(text) : null;
  if (!res.ok) {
    const msg = (json && (json.error || json.details)) || text || `Error ${res.status}`;
    throw new Error(msg);
  }
  return json;
}
