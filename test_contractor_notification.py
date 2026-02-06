import os
import requests
import json
import time
from dotenv import load_dotenv
from ghl_integration import push_to_ghl

load_dotenv()

def run_contractor_test():
    # We are simulating a lead found in Hialeah
    # But we want the SMS to go to David (689-233-0792)
    timestamp = int(time.time())
    
    lead_data = {
        "author": f"Contractor_Test_{timestamp}",
        "phone": "+16892330792", # David's phone to receive the SMS
        "text": "AC repair needed in Hialeah. Unit is leaking water.",
        "summary": "Water leak in AC unit - Hialeah emergency.",
        "niche": "HVAC",
        "location": "Hialeah, FL",
        "lead_value": 69,
        "payment_link": "https://link.fastpaydirect.com/payment-link/6983a7006503ca57b583bbf5",
        "language": "EN"
    }
    
    print(f"📡 Simulando hallazgo de Lead en Hialeah...")
    print(f"📲 Enviando notificación de subasta al contratista (David) al: {lead_data['phone']}")
    
    success = push_to_ghl(lead_data)
    
    if success:
        print("\n✅ Inyección exitosa en GHL.")
        print("👉 PASO FINAL: El workflow de GHL debería detectar el tag 'Lead de Oro' y enviarte el SMS.")
    else:
        print("\n❌ Error al inyectar en GHL. Revisa tus credenciales en el .env")

if __name__ == "__main__":
    run_contractor_test()
