import { useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Payment = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [paymentMethod, setPaymentMethod] = useState<string>("");
    const [cardNumber, setCardNumber] = useState<string>("");
    const [cardHolderName, setCardHolderName] = useState<string>("");
    const [expirationDate, setExpirationDate] = useState<string>("");
    const [cvv, setCvv] = useState<string>("");
    const [amount, setAmount] = useState<number>(0);
    const [currency, setCurrency] = useState<string>("USD");
    const [status, setStatus] = useState<string>("");

    useEffect(() => {
        if (!user) {
            navigate("/login");
        }
    }, [user, navigate]);
}