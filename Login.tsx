import { useState  } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "./Form.css";

const Login = () => {
    const { login } = useAuth();
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await login(email, password);
            navigate("/catalog"); // Redirigir tras login exitoso
        } catch {
            alert("Credenciales incorrectas");
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white shadow-md p-6 mt-10 rounded">
            <h2 className="text-2xl font-bold mb-4">Iniciar Sesión</h2>
            <form onSubmit={handleSubmit}>
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
                <button className="w-full bg-blue-500 text-white py-2 rounded">Ingresar</button>
            </form>
        </div>
    );
};

export default Login;