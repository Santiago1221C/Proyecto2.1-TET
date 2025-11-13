import hashlib

def format_tx_value(value):
    # PayU requiere 2 decimales para el cálculo de la firma, incluso si son .00
    return "{:.2f}".format(float(value))

def generate_payu_signature(merchant_id, tx_value, currency, reference_code, md5_key):
    
    #Genera la firma MD5 requerida por PayU para la integridad de la transacción.
    tx_value_str = format_tx_value(tx_value)
    
    # Usamos PAYU_MERCHANT_ID que es el ID de comercio
    signature_base = f"{md5_key}~{merchant_id}~{reference_code}~{tx_value_str}~{currency}"
    signature = hashlib.md5(signature_base.encode('utf-8')).hexdigest()
    return signature

def calculate_tax_values(amount, tax_rate=0.19):
    try:
        if tax_rate > 0:
            # Cálculo asumiendo que el monto total incluye el impuesto
            base = amount / (1 + tax_rate)
            tax = amount - base
        else:
            # Si no hay impuesto (tax_rate = 0), todo es base
            base = amount
            tax = 0
            
        # Redondeamos a dos decimales
        base_rounded = round(base, 2)
        tax_rounded = round(tax, 2)
        
        return {
            "TX_VALUE": round(base_rounded + tax_rounded, 2), # El valor total
            "TX_TAX": tax_rounded,
            "TX_TAX_RETURN_BASE": base_rounded
        }
    except Exception as e:
        print(f"Error calculating tax values: {e}")
        return {
            "TX_VALUE": amount,
            "TX_TAX": 0.00,
            "TX_TAX_RETURN_BASE": amount
        }