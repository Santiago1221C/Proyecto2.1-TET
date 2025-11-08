import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useEffect, useState } from "react";
import { getCartByUserId } from "../services/cartService";
import "./Navbar.css";

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const userId = Number(localStorage.getItem("userId")) || 1;

  const [cartItemCount, setCartItemCount] = useState(0);

  const loadCartCount = async () => {
    try {
      const cart = await getCartByUserId(userId);
      const count = cart.items?.reduce((acc: number, item: any) => acc + item.quantity, 0) || 0;
      setCartItemCount(count);
    } catch {
      setCartItemCount(0);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadCartCount();
    }
  }, [isAuthenticated]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-blue-700 text-white px-6 py-4 shadow-md">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <Link to="/" className="font-bold text-2xl hover:text-yellow-400 transition">
          BookStore
        </Link>

        {/* Navigation Links */}
        <div className="flex items-center gap-6">
          {isAuthenticated && (
            <>
              <NavLink
                to="/catalog"
                className={({ isActive }) => 
                  isActive ? "text-yellow-300 font-semibold" : "hover:text-yellow-300 transition"
                }
              >
                Catálogo
              </NavLink>

              <NavLink
                to="/cart"
                className={({ isActive }) =>
                  isActive ? "text-yellow-300 font-semibold" : "hover:text-yellow-300 transition"
                }
              >
                Carrito{" "}
                {cartItemCount > 0 && (
                  <span className="bg-yellow-300 text-blue-900 rounded-full px-2 py-0.5 ml-1 text-xs">
                    {cartItemCount}
                  </span>
                )}
              </NavLink>

              <NavLink
                to="/orders"
                className={({ isActive }) =>
                  isActive ? "text-yellow-300 font-semibold" : "hover:text-yellow-300 transition"
                }
              >
                Órdenes
              </NavLink>
            </>
          )}

          {/* Auth Controls */}
          {!isAuthenticated ? (
            <>
              <NavLink
                to="/login"
                className="hover:text-yellow-300 transition"
              >
                Login
              </NavLink>

              <NavLink
                to="/register"
                className="hover:text-yellow-300 transition"
              >
                Registrarse
              </NavLink>
            </>
          ) : (
            <button
              onClick={handleLogout}
              className="bg-red-500 px-3 py-1 rounded hover:bg-red-600 transition"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;