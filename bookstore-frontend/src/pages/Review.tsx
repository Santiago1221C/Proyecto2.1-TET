import React, { useEffect, useState } from "react";

interface Review {
  id?: string;
  userId: string;
  bookId: string;
  rating: number;
  comment: string;
  createdAt?: string;
}

const RAW_API_BASE =
  (globalThis as any)?.REACT_APP_API_BASE ||
  (globalThis as any)?.process?.env?.REACT_APP_API_BASE ||
  (window as any)?.REACT_APP_API_BASE ||
  "";

const API_BASE = RAW_API_BASE.startsWith("http") ? RAW_API_BASE.replace(/\/+$/, "") : `http://${RAW_API_BASE.replace(/\/+$/, "")}`;

const ReviewPage: React.FC = () => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [form, setForm] = useState({ userId: "", bookId: "", rating: 5, comment: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchReviews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchReviews = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/reviews`);
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      setReviews(Array.isArray(data) ? data : []);
    } catch (err: any) {
      setError(err.message || "Error al obtener reviews");
    } finally {
      setLoading(false);
    }
  };

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(await res.text());
      const created = await res.json();
      setReviews((prev) => [created, ...prev]);
      setForm({ userId: "", bookId: "", rating: 5, comment: "" });
    } catch (err: any) {
      setError(err.message || "Error al crear review");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl mb-4">Reviews</h1>

      <form onSubmit={submit} className="mb-6 space-y-2 max-w-xl">
        <div>
          <label className="block text-sm">User ID</label>
          <input className="border p-2 w-full" value={form.userId} onChange={(e) => setForm({ ...form, userId: e.target.value })} required />
        </div>
        <div>
          <label className="block text-sm">Book ID</label>
          <input className="border p-2 w-full" value={form.bookId} onChange={(e) => setForm({ ...form, bookId: e.target.value })} required />
        </div>
        <div>
          <label className="block text-sm">Rating</label>
          <input type="number" min={1} max={5} className="border p-2 w-24" value={form.rating} onChange={(e) => setForm({ ...form, rating: Number(e.target.value) })} />
        </div>
        <div>
          <label className="block text-sm">Comment</label>
          <textarea className="border p-2 w-full" value={form.comment} onChange={(e) => setForm({ ...form, comment: e.target.value })} />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
          {loading ? "Enviando..." : "Enviar review"}
        </button>
      </form>

      {error && <div className="text-red-600 mb-4">{error}</div>}

      {loading && !reviews.length ? (
        <div>Cargando reviews...</div>
      ) : (
        <ul className="space-y-4 max-w-xl">
          {reviews.map((r) => (
            <li key={r.id || `${r.userId}-${r.bookId}-${r.createdAt}`} className="border p-3 rounded">
              <div className="text-sm text-gray-600">User: {r.userId} — Book: {r.bookId} — Rating: {r.rating}</div>
              <div className="mt-2">{r.comment}</div>
              {r.createdAt && <div className="text-xs text-gray-500 mt-2">{new Date(r.createdAt).toLocaleString()}</div>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ReviewPage;
