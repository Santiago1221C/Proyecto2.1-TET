import { useEffect, useState } from "react";
import { createOrder, getAllOrdersByUserId } from "../services/orderService";
import type { Order } from "../types/Order";
import { useNavigate } from "react-router-dom";

const Orders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const userId = Number(localStorage.getItem("userId")) || 1;
  const navigate = useNavigate();

  const loadOrders = async () => {
    try {
      setLoading(true);
      const data = await getAllOrdersByUserId(userId);
      setOrders(data);
    } catch (err) {
      console.error("Error cargando órdenes:", err);
      setOrders([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOrder = async () => {
    try {
      await createOrder(userId);
      alert("¡Orden creada exitosamente!");
      loadOrders();
      navigate("/orders");
    } catch (err) {
      alert("No se pudo crear la orden.");
      console.error("Error creando orden:", err);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  if (loading) return <div className="p-6">Cargando órdenes...</div>;

  return (
    <div className="container mx-auto px-4 py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Tus Órdenes</h1>
        <button
          onClick={handleCreateOrder}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Crear orden desde carrito
        </button>
      </div>

      {!orders.length ? (
        <p className="text-gray-600">Aún no tienes órdenes realizadas.</p>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => (
            <div key={order.id} className="border p-4 rounded shadow-sm bg-white">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold">Orden #{order.id}</h2>
                <span
                  className={`px-3 py-1 rounded text-sm font-medium ${
                    order.status === "COMPLETED"
                      ? "bg-green-100 text-green-700"
                      : "bg-yellow-100 text-yellow-700"
                  }`}
                >
                  {order.status}
                </span>
              </div>

              <p className="text-sm text-gray-500 my-1">
                Fecha: {new Date(order.createdAt).toLocaleDateString()}{" "}
                {new Date(order.createdAt).toLocaleTimeString()}
              </p>

              <table className="min-w-full text-sm mt-3">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Libro</th>
                    <th className="text-left p-2">Cant.</th>
                    <th className="text-left p-2">Precio</th>
                  </tr>
                </thead>
                <tbody>
                  {order.items.map((item, idx) => (
                    <tr key={idx} className="border-b">
                      <td className="p-2">{item.title}</td>
                      <td className="p-2">{item.quantity}</td>
                      <td className="p-2">${(item.price * item.quantity).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <p className="text-right font-semibold mt-3 text-lg">
                Total: ${order.totalPrice.toFixed(2)}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders;