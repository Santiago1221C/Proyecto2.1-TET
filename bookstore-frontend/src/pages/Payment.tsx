import React, { useEffect, useState } from "react";
import { getPseBanks, checkout, API_BASE } from "../services/paymentService";
import type { PaymentCheckoutRequest, PaymentCheckoutResponse } from "../types/Payment";

const PaymentPage: React.FC = () => {
  const [method, setMethod] = useState<"CC" | "PSE">("CC");
  const [orderId, setOrderId] = useState<string>("order-1");
  const [amount, setAmount] = useState<number>(10000);
  const [responseUrl, setResponseUrl] = useState<string>(window.location.href);
  const [fullName, setFullName] = useState<string>("Test User");
  const [email, setEmail] = useState<string>("test@example.com");
  const [contactPhone, setContactPhone] = useState<string>("3000000000");

  // CC fields
  const [cardNumber, setCardNumber] = useState<string>("4111111111111111");
  const [cardExp, setCardExp] = useState<string>("2025/12");
  const [cardCvv, setCardCvv] = useState<string>("123");
  const [cardHolderName, setCardHolderName] = useState<string>("Test User");

  // PSE
  const [banks, setBanks] = useState<any[]>([]);
  const [bankCode, setBankCode] = useState<string>("");
  const [userType, setUserType] = useState<string>("PERSON");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PaymentCheckoutResponse | null>(null);

  useEffect(() => {
    if (method === "PSE") {
      getPseBanks()
        .then((data) => setBanks(data.banks || []))
        .catch(() => setBanks([]));
    }
  }, [method]);

  const onSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload: PaymentCheckoutRequest = {
      paymentMethod: method,
      order: { orderId, amount, responseUrl },
      user: {
        fullName,
        email,
        contactPhone,
      },
      deviceSessionId: "SIMULATED_SESSION",
      cookie: "SIMULATED_COOKIE",
    };

    if (method === "CC") {
      payload.card = {
        number: cardNumber,
        securityCode: cardCvv,
        expirationDate: cardExp,
        cardHolderName,
        paymentMethod: "VISA",
      };
    } else {
      payload.pse = {
        bankCode,
        userType,
      };
    }

    try {
      const res = await checkout(payload);
      setResult(res);

      if (res?.redirectionUrl) {
        window.location.href = res.redirectionUrl;
        return;
      }
    } catch (err: any) {
      setError(err?.message || String(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl mb-4">Pago (integrado con payment_service)</h1>

      <form onSubmit={onSubmit} className="space-y-3 max-w-xl">
        <div>
          <label className="block text-sm">Método</label>
          <select className="border p-2" value={method} onChange={(e) => setMethod(e.target.value as "CC" | "PSE")}>
            <option value="CC">Tarjeta de crédito (CC)</option>
            <option value="PSE">PSE</option>
          </select>
        </div>

        <div>
          <label className="block text-sm">Order ID</label>
          <input className="border p-2 w-full" value={orderId} onChange={(e) => setOrderId(e.target.value)} required />
        </div>

        <div>
          <label className="block text-sm">Amount</label>
          <input type="number" className="border p-2 w-full" value={amount} onChange={(e) => setAmount(Number(e.target.value))} required />
        </div>

        <div>
          <label className="block text-sm">Full name</label>
          <input className="border p-2 w-full" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
        </div>

        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-sm">Email</label>
            <input className="border p-2 w-full" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label className="block text-sm">Phone</label>
            <input className="border p-2 w-full" value={contactPhone} onChange={(e) => setContactPhone(e.target.value)} />
          </div>
        </div>

        {method === "CC" && (
          <>
            <div>
              <label className="block text-sm">Card number</label>
              <input className="border p-2 w-full" value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} required />
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div>
                <label className="block text-sm">Expiration (YYYY/MM)</label>
                <input className="border p-2 w-full" value={cardExp} onChange={(e) => setCardExp(e.target.value)} required />
              </div>
              <div>
                <label className="block text-sm">CVV</label>
                <input className="border p-2 w-full" value={cardCvv} onChange={(e) => setCardCvv(e.target.value)} required />
              </div>
              <div>
                <label className="block text-sm">Card holder</label>
                <input className="border p-2 w-full" value={cardHolderName} onChange={(e) => setCardHolderName(e.target.value)} required />
              </div>
            </div>
          </>
        )}

        {method === "PSE" && (
          <>
            <div>
              <label className="block text-sm">Banco</label>
              <select className="border p-2 w-full" value={bankCode} onChange={(e) => setBankCode(e.target.value)} required>
                <option value="">-- Seleccionar banco --</option>
                {banks.map((b: any) => (
                  <option key={b.code || b.bankCode || b.bankId} value={b.code || b.bankCode || b.bankId}>
                    {b.name || b.bankName || b.description}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm">Tipo de usuario (PSE)</label>
              <select className="border p-2 w-full" value={userType} onChange={(e) => setUserType(e.target.value)}>
                <option value="PERSON">PERSON</option>
                <option value="BUSINESS">BUSINESS</option>
              </select>
            </div>

            <div>
              <label className="block text-sm">Response URL (para redirección PSE)</label>
              <input className="border p-2 w-full" value={responseUrl} onChange={(e) => setResponseUrl(e.target.value)} required />
            </div>
          </>
        )}

        <div>
          <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded" disabled={loading}>
            {loading ? "Procesando..." : "Iniciar pago"}
          </button>
        </div>
      </form>

      {error && <div className="text-red-600 mt-4">{error}</div>}

      {result && (
        <div className="border p-3 rounded mt-4 max-w-xl">
          <div className="mb-2 font-medium">Respuesta del servicio:</div>
          <pre className="text-sm bg-gray-100 p-2 rounded overflow-auto">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      <div className="text-xs text-gray-500 mt-4">
        Nota: se realiza GET {API_BASE}/banks/pse y POST {API_BASE}/checkout. Asegura CORS en payment_service y que REACT_APP_API_BASE incluya host (el código añade http:// si falta).
      </div>
    </div>
  );
};

export default PaymentPage;
