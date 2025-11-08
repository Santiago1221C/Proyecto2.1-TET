import { useEffect, useState } from "react";
import { getAllBooks } from "../services/catalogService";
import { createCart, addItemToCart } from "../services/cartService";
import type { Book } from "../types/Book";

const Catalog = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState<Record<number, boolean>>({});
  const userId = Number(localStorage.getItem("userId")) || 1;

  useEffect(() => {
    let mounted = true;

    const load = async () => {
      try {
        setLoading(true);
        const data = await getAllBooks();
        if (mounted) setBooks(data);
      } catch (err) {
        console.error("Error cargando libros:", err);
        setBooks([]);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    load();
    return () => {
      mounted = false;
    };
  }, []);

  const handleAddToCart = async (book: Book, qty = 1) => {
    try {
      setAdding((prev) => ({ ...prev, [book.id]: true }));
      await createCart(userId);

      const itemPayload = {
        bookId: book.id,
        title: book.title,
        author: book.author,
        price: book.price,
        quantity: qty,
      };

      const updatedCart = await addItemToCart(userId, itemPayload);
      console.log("Carrito actualizado:", updatedCart);

      alert(`"${book.title}" agregado al carrito.`);
    } catch (err) {
      alert("Error al agregar al carrito. Revisa la consola.");
      console.error("Error:", err);
    } finally {
      setAdding((prev) => ({ ...prev, [book.id]: false }));
    }
  };

  if (loading) return <div className="p-6">Cargando catálogo...</div>;
  if (!books.length) return <div className="p-6">No hay libros disponibles.</div>;

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-3xl font-bold mb-6">Catálogo</h1>
      <div className="grid gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        {books.map((b) => (
          <div
            key={b.id}
            className="bg-white border rounded-lg shadow-md hover:shadow-xl transition-shadow duration-200 p-4 flex flex-col justify-between"
          >
            <div>
              <h2 className="text-xl font-semibold">{b.title}</h2>
              <p className="text-sm text-gray-500 mt-1">por {b.author}</p>
              <p className="mt-3 text-sm text-gray-700">{b.description}</p>
            </div>
            <div className="mt-4 flex items-center justify-between">
              <div>
                <p className="text-lg font-bold text-blue-600">
                  ${b.price?.toFixed(2)}
                </p>
                <p className="text-xs text-gray-500">Stock: {b.stock ?? 0}</p>
              </div>
              <button
                disabled={adding[b.id] || !b.stock}
                onClick={() => handleAddToCart(b, 1)}
                className={`px-3 py-1 rounded-md text-white font-medium transition ${
                  !b.stock
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                {adding[b.id]
                  ? "Agregando..."
                  : b.stock
                  ? "Agregar"
                  : "Sin stock"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Catalog;
