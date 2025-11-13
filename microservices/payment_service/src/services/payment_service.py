import requests
import os
import json
from src.utils.payu_utils import generate_payu_signature, calculate_tax_values

# Cargar configuración desde environment
PAYU_API_KEY = os.getenv("PAYU_API_KEY", "4Vj8eK4rloUO70w0KzSXXXX")     
PAYU_MERCHANT_ID = os.getenv("PAYU_MERCHANT_ID", "508029")              
PAYU_ACCOUNT_ID = os.getenv("PAYU_ACCOUNT_ID", "512321")              
PAYU_MD5_KEY = os.getenv("PAYU_MD5_KEY", "4Vj8eK4rloUO70w0KzSXXXX")    
PAYU_API_URL = os.getenv("PAYU_API_URL", "https://sandbox.api.payulatam.com/payments-api/4.0/service.cgi")
CURRENCY = "COP" # Asumimos COP para Colombia

def submit_transaction(payload):
    """Envía la solicitud de pago o consulta a la API de PayU."""
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    
    try:
        response = requests.post(PAYU_API_URL, headers=headers, json=payload)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error comunicándose con la API de PayU: {e}")
        # Retorna una estructura de error consistente para ser manejada por la ruta
        return {"code": "ERROR", "error": f"API Request Failed: {e}"}

# --- Funciones de Utilidad ---

def get_pse_banks():

    payload = {
        "language": "es",
        "command": "GET_BANKS_LIST",
        "merchant": {
            "apiLogin": PAYU_API_KEY,
            "apiKey": PAYU_API_KEY # PayU usa API Key para apiLogin en Sandbox/pruebas
        },
        "test": True,
        "bankListInformation": {
            "paymentMethod": "PSE",
            "paymentCountry": "CO"
        }
    }
    return submit_transaction(payload)


def build_pse_payload(order_data, user_data, pse_data, client_data):

    amount = order_data['amount']
    reference_code = f"ORDER-PSE-{order_data['orderId']}"
    
    # 1. Calcular valores de impuestos
    calculated_values = calculate_tax_values(amount)
    
    # 2. Generar firma
    signature = generate_payu_signature(
        PAYU_MERCHANT_ID, calculated_values['TX_VALUE'], CURRENCY, reference_code, PAYU_MD5_KEY
    )

    # 3. Construir el payload
    payload = {
        "test": True, 
        "language": "es",
        "command": "SUBMIT_TRANSACTION",
        "merchant": {
            "apiKey": PAYU_API_KEY,
            "apiLogin": PAYU_API_KEY 
        },
        "transaction": {
            "type": "AUTHORIZATION_AND_CAPTURE",
            "paymentMethod": "PSE",
            "paymentCountry": "CO",
            "deviceSessionId": client_data.get('deviceSessionId', 'SIMULATED_SESSION_ID'),
            "ipAddress": client_data.get('ipAddress', '127.0.0.1'),
            "cookie": client_data.get('cookie', 'SIMULATED_COOKIE'),
            "userAgent": client_data.get('userAgent', 'SIMULATED_USER_AGENT'),
            "order": {
                "accountId": PAYU_ACCOUNT_ID,
                "referenceCode": reference_code,
                "description": f"Bookstore purchase - PSE Order #{order_data['orderId']}",
                "language": "es",
                "signature": signature,
                "notifyUrl": order_data.get('notifyUrl', 'http://yourdomain.com/payu/notify'),
                "additionalValues": {
                    "TX_VALUE": {
                        "value": calculated_values['TX_VALUE'],
                        "currency": CURRENCY
                    },
                    "TX_TAX": {
                        "value": calculated_values['TX_TAX'],
                        "currency": CURRENCY
                    },
                    "TX_TAX_RETURN_BASE": {
                        "value": calculated_values['TX_TAX_RETURN_BASE'],
                        "currency": CURRENCY
                    }
                },
                "buyer": {
                    "fullName": user_data['fullName'],
                    "emailAddress": user_data['email'],
                    "contactPhone": user_data['contactPhone'],
                    "dniNumber": user_data['dniNumber'],
                    "shippingAddress": user_data['shippingAddress'] # Asumimos que la estructura es completa
                }
            },
            "payer": {
                "fullName": user_data['fullName'],
                "emailAddress": user_data['email'],
                "contactPhone": user_data['contactPhone'],
                "dniNumber": user_data['dniNumber'],
                "dniType": user_data.get('dniType', 'CC'), 
                "billingAddress": user_data['shippingAddress'] # Usamos la misma dirección para facturación PSE
            },
            "extraParameters": {
                "RESPONSE_URL": order_data['responseUrl'], # Obligatorio para redirección PSE
                "FINANCIAL_INSTITUTION_CODE": pse_data['bankCode'], # Código del banco
                "USER_TYPE": pse_data['userType'] # N o J
            }
        }
    }
    return payload

# Función de Tarjeta de Crédito

def build_cc_payload(order_data, user_data, card_data, client_data):
    """
    Construye el payload completo de PayU para Tarjeta de Crédito/Débito.
    """
    amount = order_data['amount']
    reference_code = f"ORDER-CC-{order_data['orderId']}"
    
    # 1. Calcular valores de impuestos
    calculated_values = calculate_tax_values(amount)
    
    # 2. Generar firma
    signature = generate_payu_signature(
        PAYU_MERCHANT_ID, calculated_values['TX_VALUE'], CURRENCY, reference_code, PAYU_MD5_KEY
    )

    # 3. Construir el payload con campos OBLIGATORIOS (mínimos)
    payload = {
        "test": True, 
        "language": "es",
        "command": "SUBMIT_TRANSACTION",
        "merchant": {
            "apiKey": PAYU_API_KEY,
            "apiLogin": PAYU_API_KEY 
        },
        "transaction": {
            "type": "AUTHORIZATION_AND_CAPTURE",
            "paymentMethod": card_data.get('paymentMethod', 'VISA'),
            "paymentCountry": "CO",
            "deviceSessionId": client_data.get('deviceSessionId', 'SIMULATED_SESSION_ID'),
            "ipAddress": client_data.get('ipAddress', '127.0.0.1'),
            "cookie": client_data.get('cookie', 'SIMULATED_COOKIE'),
            "userAgent": client_data.get('userAgent', 'SIMULATED_USER_AGENT'),
            "order": {
                "accountId": PAYU_ACCOUNT_ID,
                "referenceCode": reference_code,
                "description": f"Bookstore purchase - CC Order #{order_data['orderId']}",
                "language": "es",
                "signature": signature,
                "additionalValues": {
                    "TX_VALUE": {
                        "value": calculated_values['TX_VALUE'],
                        "currency": CURRENCY
                    },
                    "TX_TAX": {
                        "value": calculated_values['TX_TAX'],
                        "currency": CURRENCY
                    },
                    "TX_TAX_RETURN_BASE": {
                        "value": calculated_values['TX_TAX_RETURN_BASE'],
                        "currency": CURRENCY
                    }
                },
                "buyer": {
                    "fullName": user_data['fullName'],
                    "emailAddress": user_data['email'],
                    "contactPhone": user_data['contactPhone'],
                    "dniNumber": user_data['dniNumber'],
                    "shippingAddress": user_data['shippingAddress']
                }
            },
            "creditCard": {
                "number": card_data['number'], 
                "securityCode": card_data['securityCode'],
                "expirationDate": card_data['expirationDate'], 
                "name": card_data['cardHolderName']
            },
            "payer": {
                "fullName": card_data['cardHolderName'],
                "emailAddress": user_data['email'],
                "contactPhone": user_data['contactPhone'],
                "dniNumber": user_data['dniNumber'],
                "billingAddress": user_data['shippingAddress'] # Usamos la misma dirección para facturación
            }
        }
    }
    return submit_transaction(payload)