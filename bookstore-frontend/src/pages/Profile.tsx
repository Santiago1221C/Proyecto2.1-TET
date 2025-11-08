import { useState, useEffect } from "react";
import { getUserProfile, updateProfile } from "../services/userService";

// Definición simple de tipos (deberían estar en ../types/User.ts)
type UserProfile = { userId: number; name: string; email: string; address: string };
type UserUpdateData = Partial<UserProfile>;

const Profile = () => {
  const userId = Number(localStorage.getItem("userId")) || 1; // ID del usuario actual
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState<UserUpdateData>({});
  const [message, setMessage] = useState<string | null>(null);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const data = await getUserProfile(userId);
      setUser(data);
      setEditData(data);
    } catch (err) {
      console.error("Error al cargar perfil:", err);
      setUser(null);
      setMessage("No se pudo cargar la información del perfil.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);
    try {
      const updatedUser = await updateProfile(userId, editData);
      setUser(updatedUser);
      setIsEditing(false);
      setMessage("Perfil actualizado exitosamente.");
    } catch (err) {
      console.error("Error al actualizar:", err);
      setMessage("Error al actualizar el perfil.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-6">Cargando perfil...</div>;
  if (!user) return <div className="p-6 text-red-600">{message || "Usuario no encontrado."}</div>;

  return (
    <div className="container mx-auto px-4 py-6 max-w-lg">
      <h1 className="text-3xl font-bold mb-6">👤 Mi Perfil</h1>
      
      {message && <div className={`mb-4 p-3 rounded ${message.includes("exitosamente") ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>{message}</div>}

      {isEditing ? (
        <form onSubmit={handleUpdate} className="space-y-4 bg-white shadow-md rounded-lg p-6">
          <label className="block">Nombre: <input type="text" value={editData.name || ''} onChange={(e) => setEditData({...editData, name: e.target.value})} className="mt-1 block w-full border rounded p-2" required /></label>
          <label className="block">Email: <input type="email" value={editData.email || ''} onChange={(e) => setEditData({...editData, email: e.target.value})} className="mt-1 block w-full border rounded p-2" disabled /></label>
          <label className="block">Dirección: <input type="text" value={editData.address || ''} onChange={(e) => setEditData({...editData, address: e.target.value})} className="mt-1 block w-full border rounded p-2" /></label>
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={() => { setIsEditing(false); setEditData(user); setMessage(null); }} className="px-4 py-2 border rounded hover:bg-gray-100">Cancelar</button>
            <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Guardar Cambios</button>
          </div>
        </form>
      ) : (
        <div className="bg-white shadow-md rounded-lg p-6 space-y-3">
          <p><strong>Nombre:</strong> {user.name}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Dirección:</strong> {user.address || 'N/A'}</p>
          <div className="pt-2">
            <button onClick={() => setIsEditing(true)} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Editar Perfil</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Profile;