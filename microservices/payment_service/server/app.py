import os
from flask import Flask, jsonify
from src.routes.payment_routes import payment_bp 

# Las credenciales se definen como variables de entorno
# Usar credenciales de Sandbox de PayU para pruebas
os.environ['PAYU_API_KEY'] = "4Vj8eK4rloUO70w0KzSXXXX" 
os.environ['PAYU_MD5_KEY'] = "4Vj8eK4rloUO70w0KzSXXXX"
os.environ['PAYU_MERCHANT_ID'] = "508029" 
os.environ['PAYU_ACCOUNT_ID'] = "512321" 

SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8084))

app = Flask(__name__)

# Registrar el Blueprint para incluir las rutas bajo /api/v1/payment
app.register_blueprint(payment_bp, url_prefix='/api/v1/payment')

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud."""
    return jsonify({"status": "Payment Service Operational"}), 200

if __name__ == '__main__':
    # Usar un try-except simple para garantizar que la app inicia
    try:
        print(f"Starting Payment Service on port {SERVICE_PORT}...")
        app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)
    except Exception as e:
        print(f"Failed to start server: {e}")