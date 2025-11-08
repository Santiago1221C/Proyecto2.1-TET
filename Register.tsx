import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Register = () => {
    const { register } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await register(email, password, username);
            alert("Registro exitoso, ahora inicia sesión");
            navigate("/login");
        } catch {
            alert("Error al registrarse");
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white shadow-md p-6 mt-10 rounded">
            <h2 className="text-2xl font-bold mb-4">Registrarse</h2>
            <form onSubmit={handleSubmit}>
                <input
                    className="w-full p-2 border rounded mb-4"
                    type="text"
                    placeholder="Nombre de usuario"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    className="w-full p-2 border rounded mb-4"
                    type="email"
                    placeholder="Correo electrónico"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input 
                    className="w-full p-2 border rounded mb-4"
                    type="password"
                    placeholder="Contraseña"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button className="w-full bg-green-500 text-white py-2 rounded">Registrarse</button>
            </form>
        </div>
    );
};

export default Register;