import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def push_to_ghl(lead_data):
    """
    Pushes a verified gold lead to GoHighLevel with auction details for contractors.
    """
    api_key = os.getenv("GHL_API_KEY", "").strip()
    location_id = os.getenv("GHL_LOCATION_ID", "").strip()
    
    # Load templates (Auction style for contractors)
    templates_path = os.path.join(os.path.dirname(__file__), "message_templates.json")
    try:
        with open(templates_path, 'r', encoding='utf-8') as f:
            templates = json.load(f)
    except Exception as e:
        print(f"⚠️ Warning: Could not load templates: {e}")
        templates = {}

    url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # FastPay / Stripe link for this specific niche
    payment_link = lead_data.get('payment_link', 'https://link.fastpaydirect.com/payment-link/6983a7006503ca57b583bbf5')
    lang = lead_data.get('language', 'EN').lower()
    
    # Format the message intended for CONTRACTORS (The Auction)
    auction_sms = ""
    if templates and "auction" in templates:
        # Default for contractors (usually same as lead lang or based on market)
        lang_templates = templates["auction"].get(lang, templates["auction"].get("es", {}))
        template_text = lang_templates.get("sms", "")
        auction_sms = template_text.format(
            niche=lead_data['niche'],
            location=lead_data['location'],
            lead_value=lead_data.get('lead_value', 65),
            summary=lead_data.get('summary', 'Urgent service request'),
            payment_link=f"{payment_link}?lead_id={{contact.id}}" # Exclusivity ID added here
        )

    payload = {
        "firstName": lead_data['author'].split()[0],
        "lastName": lead_data['author'].split()[-1] if len(lead_data['author'].split()) > 1 else "Lead",
        "phone": lead_data.get('phone', '+17865550000'), 
        "locationId": location_id,
        "tags": ["Lead de Oro", f"nicho: {lead_data['niche']}", "disponible", f"lang: {lang.lower()}"],
        "customField": {
            "intent_summary": lead_data['summary'],
            "original_review": lead_data['text'],
            "lead_value": lead_data.get('lead_value', 65),
            "payment_link": f"{payment_link}?lead_id={{contact.id}}",
            "auction_message": auction_sms, 
            "niche_name": lead_data['niche'],
            "lead_location": lead_data['location']
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Lead '{lead_data['author']}' inyectado para SUBASTA en GHL.")
            return True
        else:
            print(f"❌ Error GHL: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error GHL: {e}")
        return False
