import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { initiatePayment } from "../services/paymentService";
// Se puede necesitar Order Service para obtener detalles de la orden, si no se tienen.

const Payment = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Simulación: Obtener orderId y amount de la URL o del estado
  const query = new URLSearchParams(location.search);
  const orderId = Number(query.get("orderId")) || 0;
  // Usamos una cantidad de ejemplo si no está en el query. En producción, se obtiene del Order Service.
  const amount = Number(query.get("amount")) || 100.00; 
  const userId = Number(localStorage.getItem("userId")) || 1;

  useEffect(() => {
    if (orderId === 0 || amount === 0) {
      setError("Faltan detalles de la orden para proceder al pago.");
      return;
    }
    
    // Iniciar pago automáticamente al cargar la página
    handleInitiatePayment();
  }, [orderId, amount]);

  const handleInitiatePayment = async () => {
    setLoading(true);
    setError(null);
    try {
      const { redirectUrl } = await initiatePayment(orderId, amount);
      
      if (redirectUrl) {
        // Redirigir al usuario a la pasarela de pagos de terceros (Stripe/PayPal)
        window.location.href = redirectUrl;
        // La pasarela nos devolverá a /payment/success o /payment/cancel
      } else {
         // Esto ocurriría si el Payment Service procesa el pago internamente y sin redirección
        setError("El Payment Service no devolvió una URL de pago. Verifique el backend.");
      }

    } catch (err) {
      console.error("Error al iniciar el pago:", err);
      setError("Error al comunicar con la pasarela de pagos. Por favor, inténtalo de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <div className="p-6 text-center text-red-600">
        <h1 className="text-2xl font-bold mb-4">Error de Pago</h1>
        <p>{error}</p>
        <button onClick={() => navigate("/cart")} className="mt-4 px-4 py-2 bg-gray-200 rounded">
          Volver al Carrito
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="p-6 text-center">
        <h1 className="text-2xl font-bold mb-4">Redirigiendo a Pasarela de Pago...</h1>
        <p>Procesando orden **#{orderId}** por **${amount.toFixed(2)} USD**.</p>
        <p className="mt-4">Por favor, espera.</p>
      </div>
    );
  }

  // Si no se redirigió y no hay error, es una vista de espera
  return (
    <div className="p-6 text-center">
      <h1 className="text-2xl font-bold mb-4">Esperando Redirección</h1>
      <p>Si la redirección no ocurre, contacta a soporte.</p>
    </div>
  );
};

export default Payment;