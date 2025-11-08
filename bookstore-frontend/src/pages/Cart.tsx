import { useEffect, useState } from "react";
import { getCartByUserId, addItemToCart, removeItemFromCart, clearCart} from "../services/cartService";
import type { Cart as CartType, CartItem } from "../types/Cart";
import { useNavigate } from "react-router-dom";
import { createOrder } from "../services/orderService";

const Cart = () => {
  const [cart, setCart] = useState<CartType | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const userId = Number(localStorage.getItem("userId")) || 1;
  const navigate = useNavigate();

  const loadCart = async () => {
    try {
      setLoading(true);
      const data = await getCartByUserId(userId);
      setCart(data);
    } catch (err) {
      console.error("Error cargando carrito:", err);
      setCart(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCart();
  }, []);

  const updateItemQuantity = async (item: CartItem, increment: boolean) => {
    try {
      setProcessing(true);
      const updatedQuantity = increment
        ? item.quantity + 1
        : item.quantity - 1;

      if (updatedQuantity <= 0) {
        await removeItemFromCart(userId, item.bookId);
      } else {
        await addItemToCart(userId, {
          ...item,
          quantity: increment ? 1 : -1, // Solo mandamos diferencia
        });
      }

      loadCart();
    } catch (err) {
      alert("Error al modificar cantidad.");
      console.error("Error:", err);
    } finally {
      setProcessing(false);
    }
  };

  const handleRemoveItem = async (bookId: number) => {
    try {
      setProcessing(true);
      await removeItemFromCart(userId, bookId);
      loadCart();
    } catch (err) {
      alert("Error al eliminar ítem.");
    } finally {
      setProcessing(false);
    }
  };

  const handleClearCart = async () => {
    try {
      setProcessing(true);
      await clearCart(userId);
      loadCart();
    } catch (err) {
      alert("Error al vaciar carrito.");
    } finally {
      setProcessing(false);
    }
  };

  const handleProceedToOrder = async () => {
    try {
      setProcessing(true);
      await createOrder(userId);
      alert("¡Orden creada exitosamente!");
      navigate("/orders");
    } catch (err) {
      alert("Error al crear orden.");
      console.error("Error:", err);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) return <div className="p-6">Cargando carrito...</div>;
  if (!cart || !cart.items.length)
    return <div className="p-6">Tu carrito está vacío.</div>;

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-3xl font-bold mb-6">Tu Carrito</h1>

      <div className="bg-white shadow-md rounded-lg p-4 space-y-4">
        {cart.items.map((item) => (
          <div
            key={item.bookId}
            className="flex justify-between items-center border-b pb-3"
          >
            <div>
              <p className="font-semibold">{item.title}</p>
              <p className="text-sm text-gray-500">por {item.author}</p>
              <p className="mt-1 text-sm">Precio: ${item.price.toFixed(2)}</p>
            </div>

            <div className="flex items-center space-x-2">
              <button
                disabled={processing}
                onClick={() => updateItemQuantity(item, false)}
                className="px-2 py-1 border rounded hover:bg-gray-100"
              >
                -
              </button>
              <span className="px-2">{item.quantity}</span>
              <button
                disabled={processing}
                onClick={() => updateItemQuantity(item, true)}
                className="px-2 py-1 border rounded hover:bg-gray-100"
              >
                +
              </button>
              <button
                disabled={processing}
                onClick={() => handleRemoveItem(item.bookId)}
                className="ml-4 text-red-500 hover:text-red-700"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 flex justify-between items-center">
        <div className="text-xl font-bold">
          Total: ${cart.totalPrice.toFixed(2)}
        </div>
        <div className="space-x-3">
          <button
            disabled={processing}
            onClick={handleClearCart}
            className="px-4 py-2 border rounded hover:bg-gray-100"
          >
            Vaciar carrito
          </button>
          <button
            disabled={processing}
            onClick={handleProceedToOrder}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Proceder a Orden
          </button>
        </div>
      </div>
    </div>
  );
};

export default Cart;