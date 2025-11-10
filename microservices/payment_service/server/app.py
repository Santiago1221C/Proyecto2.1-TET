import os
import hashlib
import requests
import json
from flask import Flask, request, jsonify

# Credenciales Hardcodeadas de PayU Sandbox ===
# Estas claves son de ejemplo.
# Se ponen aquí temporalmente por no usar un archivo .env.

PAYU_API_KEY = "4Vj8eK4rloUO70w0KzSXXXX"    # Clave de API
PAYU_MERCHANT_ID = "508029"                 # ID de Comercio
PAYU_ACCOUNT_ID = "512321"                  # ID de Cuenta
PAYU_MD5_KEY = "4Vj8eK4rloUO70w0KzSXXXX"    # Clave para Signature
PAYU_API_URL = "https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi"

SERVICE_PORT = int(os.getenv("SERVICE_PORT", 8084))
SUCCESS_STATUS = ["APPROVED", "PENDING"] # Estados que indican éxito o procesamiento

app = Flask(__name__)

def generate_payu_signature(merchant_id, tx_value, currency, reference_code, md5_key):
    """
    Generates the MD5 signature required by PayU for transaction integrity.
    Format: <MD5_KEY>~<MERCHANT_ID>~<REFERENCE_CODE>~<TX_VALUE>~<CURRENCY>
    """
    tx_value_str = "{:.2f}".format(tx_value)
    signature_base = f"{md5_key}~{merchant_id}~{reference_code}~{tx_value_str}~{currency}"
    signature = hashlib.md5(signature_base.encode('utf-8')).hexdigest()
    return signature

def create_payu_payload(order_data, user_data, simulated_card_data):
    """
    Builds the complete PayU request payload for a Credit Card transaction.
    """
    tx_value = order_data['amount']
    currency = order_data.get('currency', 'USD')
    reference_code = f"ORDER-{order_data['orderId']}"
    
    # 1. Generate signature
    signature = generate_payu_signature(
        PAYU_MERCHANT_ID, tx_value, currency, reference_code, PAYU_MD5_KEY
    )

    # 2. Build transaction object
    payload = {
        "test": True, 
        "language": "es",
        "command": "SUBMIT_TRANSACTION",
        "merchant": {
            "apiKey": PAYU_API_KEY,
            "apiLogin": PAYU_API_KEY
        },
        "transaction": {
            "order": {
                "accountId": PAYU_ACCOUNT_ID,
                "referenceCode": reference_code,
                "description": f"Bookstore purchase - Order #{order_data['orderId']}",
                "language": "es",
                "signature": signature,
                "additionalValues": {
                    "TX_VALUE": {
                        "value": tx_value,
                        "currency": currency
                    }
                },
                "buyer": {
                    "merchantBuyerId": user_data['id'],
                    "fullName": user_data['fullName'],
                    "emailAddress": user_data['email'],
                }
            },
            "payer": {
                "fullName": simulated_card_data['cardHolderName'],
                "emailAddress": user_data['email'],
                "dniNumber": user_data.get('dni', 'N/A')
            },
            "creditCard": {
                # Test card that results in APPROVED in PayU Sandbox
                "number": "4111111111111111", 
                "securityCode": "123",
                "expirationDate": "2030/12", # YYYY/MM
                "name": simulated_card_data['cardHolderName']
            },
            "type": "AUTHORIZATION_AND_CAPTURE",
            "paymentMethod": "VISA",
            "paymentCountry": "CO",
            "deviceSessionId": "SIMULATED_SESSION_ID",
            "ipAddress": "127.0.0.1" 
        }
    }
    return payload


@app.route('/checkout', methods=['POST'])
def initiate_checkout():
    """
    Endpoint to initiate the payment process by calling the PayU Sandbox API.
    """
    data = request.json
    order_id = data.get('orderId')
    amount = data.get('amount')
    
    if not order_id or not amount:
        return jsonify({"error": "Missing orderId or amount"}), 400

    try:
        # --- 1. SIMULATED DATA FETCHING (In a real scenario, call other services) ---
        user_id = "12345" 
        user_data = {
            "id": user_id,
            "fullName": "Test Buyer",
            "email": "test@payu.com",
            "dni": "1000000000"
        }

        order_data = {
            "orderId": order_id,
            "amount": amount,
            "currency": data.get('currency', 'USD')
        }

        simulated_card_data = {
            "cardNumber": "4111111111111111", 
            "cvc": "123",
            "expiryDate": "2030/12", 
            "cardHolderName": "Test Buyer"
        }
        
        # Ensure successUrl and cancelUrl are available
        success_url = data.get('successUrl', '/payment/success')
        cancel_url = data.get('cancelUrl', '/payment/cancel')


        # --- 2. CREATE PAYLOAD AND CALL PAYU ---
        payu_payload = create_payu_payload(order_data, user_data, simulated_card_data)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        
        response = requests.post(PAYU_API_URL, headers=headers, json=payu_payload)
        response.raise_for_status() 
        
        payu_response = response.json()
        
        # --- 3. PROCESS PAYU RESPONSE ---
        transaction_status = payu_response.get('transactionResponse', {}).get('state')
        
        if transaction_status in SUCCESS_STATUS:
            # Payment APPROVED or PENDING
            return jsonify({
                "message": "Transaction successful", 
                "transactionId": payu_response.get('transactionResponse', {}).get('transactionId'),
                "redirectUrl": success_url 
            }), 200
        else:
            # Transaction REJECTED or ERROR
            error_message = payu_response.get('transactionResponse', {}).get('responseMessage', 'Transaction rejected')
            
            return jsonify({
                "error": "Payment failed",
                "details": error_message,
                "redirectUrl": cancel_url
            }), 400
            
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with PayU API: {e}")
        return jsonify({
            "error": "External payment service error",
            "redirectUrl": data.get('cancelUrl', '/payment/cancel')
        }), 503
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({
            "error": "Internal server error",
            "redirectUrl": data.get('cancelUrl', '/payment/cancel')
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=True)