from flask import Blueprint, request, jsonify
from src.services.payment_service import build_cc_payload, build_pse_payload, get_pse_banks

# Definimos el Blueprint para las rutas de pago
payment_bp = Blueprint('payment', __name__)

# Estados que indican una transacción exitosa o en proceso
SUCCESS_STATUS = ["APPROVED", "PENDING"]

@payment_bp.route('/banks/pse', methods=['GET'])
def list_pse_banks():
    try:
        payu_response = get_pse_banks()
        
        if payu_response.get('code') == "SUCCESS":
            return jsonify({
                "code": "SUCCESS",
                "banks": payu_response.get('banks', [])
            }), 200
        else:
            return jsonify({
                "error": "Fallo al obtener la lista de bancos PayU", 
                "details": payu_response.get('error')
            }), 400
            
    except Exception as e:
        print(f"Error inesperado al listar bancos PSE: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@payment_bp.route('/checkout', methods=['POST'])
def initiate_checkout():
    data = request.json
    
    # 1. Validación de datos de entrada mínimos y método de pago
    method = data.get('paymentMethod')
    if method not in ["CC", "PSE"]:
        return jsonify({"error": "paymentMethod debe ser 'CC' o 'PSE'"}), 400
    if not all(k in data.get('order', {}) for k in ('orderId', 'amount')):
        return jsonify({"error": "Faltan datos de orden (orderId o amount)"}), 400
    if not data.get('user'):
        return jsonify({"error": "Faltan datos de usuario"}), 400

    try:
        order_data = data['order']
        user_data = data['user']
        
        # Obtener datos de la sesión del cliente
        client_data = {
            "ipAddress": request.remote_addr, 
            "userAgent": request.headers.get('User-Agent'),
            "deviceSessionId": data.get('deviceSessionId', 'SIMULATED_SESSION_ID'),
            "cookie": data.get('cookie', 'SIMULATED_COOKIE')
        }

        payu_response = {}
        
        if method == "CC":
            if not data.get('card'):
                 return jsonify({"error": "Faltan datos de tarjeta para el método CC"}), 400
            # Llamada al servicio de tarjeta de crédito
            payu_response = build_cc_payload(order_data, user_data, data['card'], client_data)
        
        elif method == "PSE":
            if not data.get('pse') or not order_data.get('responseUrl'):
                 return jsonify({"error": "Faltan datos PSE (bankCode, userType) o responseUrl"}), 400
            # Llamada al servicio de pago PSE
            payu_response = build_pse_payload(order_data, user_data, data['pse'], client_data)
        
        # 2. Procesar Respuesta PayU (Unificada)
        transaction_response = payu_response.get('transactionResponse', {})
        transaction_status = transaction_response.get('state')
        
        # Extracción de campos detallados
        detailed_response = {
            "transactionId": transaction_response.get('transactionId'),
            "orderId": transaction_response.get('orderId'),
            "state": transaction_status,
            "responseCode": transaction_response.get('responseCode'),
            "paymentNetworkResponseCode": transaction_response.get('paymentNetworkResponseCode'),
            "trazabilityCode": transaction_response.get('trazabilityCode'),
            "authorizationCode": transaction_response.get('authorizationCode'),
            "responseMessage": transaction_response.get('responseMessage'),
            "operationDate": transaction_response.get('operationDate')
        }
        
        if payu_response.get('code') == "SUCCESS" and transaction_status in SUCCESS_STATUS:
            
            if method == "PSE":
                # PSE: Retorna la URL de redirección
                redirection_url = transaction_response.get('extraParameters', {}).get('BANK_URL')
                return jsonify({
                    "message": "Redirección a PSE pendiente", 
                    "status": transaction_status,
                    "redirectionUrl": redirection_url,
                    "details": detailed_response
                }), 200
            else:
                # CC: Retorna el estado final
                return jsonify({
                    "message": "Transacción procesada correctamente", 
                    "status": transaction_status,
                    "details": detailed_response
                }), 200
        else:
            # Transacción RECHAZADA o ERROR de API
            error_message = payu_response.get('error') or transaction_response.get('responseMessage', 'Transacción rechazada o fallida')
            
            return jsonify({
                "error": "Fallo en el pago",
                "details": error_message,
                "status": transaction_status or 'ERROR',
                "payuResponseDetails": detailed_response 
            }), 400
            
    except Exception as e:
        print(f"Error inesperado al procesar el checkout: {e}")
        return jsonify({"error": "Error interno del servidor", "status": "INTERNAL_ERROR"}), 500