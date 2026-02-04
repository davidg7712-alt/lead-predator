import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def push_to_ghl(lead_data):
    """
    Pushes a verified gold lead to GoHighLevel with its specific payment link and exclusivity metadata.
    """
    api_key = os.getenv("GHL_API_KEY", "").strip()
    location_id = os.getenv("GHL_LOCATION_ID", "").strip()
    
    url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # We include the specific payment link for this niche
    payment_link = lead_data.get('payment_link', 'https://link.fastpaydirect.com/payment-link/6983a7006503ca57b583bbf5')
    
    payload = {
        "firstName": lead_data['author'].split()[0],
        "lastName": lead_data['author'].split()[-1] if len(lead_data['author'].split()) > 1 else "Lead",
        "phone": lead_data.get('phone', '+17865550000'), # Default if not found yet
        "locationId": location_id,
        "tags": ["Lead de Oro", f"Nicho: {lead_data['niche']}", "Disponible"],
        "customField": {
            "intent_summary": lead_data['summary'],
            "original_review": lead_data['text'],
            "niche_price": lead_data.get('lead_value', 65),
            "payment_link_niche": f"{payment_link}?lead_id={{contact.id}}" # Adding the Exclusivity ID
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Lead '{lead_data['author']}' (Tel: {payload['phone']}) inyectado en GHL.")
            return True
        else:
            print(f"❌ Error GHL: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error GHL: {e}")
        return False
