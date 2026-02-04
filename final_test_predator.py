import os
import json
import requests
from dotenv import load_dotenv
from UniversalScraper import UniversalScraper

load_dotenv()

def push_to_ghl(lead_data):
    """
    Pushes a verified gold lead to GoHighLevel as a New Contact.
    """
    api_key = os.getenv("GHL_API_KEY")
    location_id = os.getenv("GHL_LOCATION_ID")
    
    url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # We simulate a phone number for the lead
    payload = {
        "firstName": lead_data['author'].split()[0],
        "lastName": lead_data['author'].split()[-1] if len(lead_data['author'].split()) > 1 else "",
        "phone": "+17865550911", # Demo Phone
        "locationId": location_id,
        "tags": ["Lead de Oro", "Miami HVAC", "Live Test"],
        "customField": {
            "intent_summary": lead_data['summary'],
            "original_review": lead_data['text']
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Lead 'REAL' de '{lead_data['author']}' inyectado con éxito en GHL.")
            return True
        else:
            print(f"❌ Error inyectando lead: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error GHL: {e}")
        return False

def run_live_test():
    scraper = UniversalScraper()
    
    # Simulating a REAL High-Urgency Case
    live_case = {
        "author": "Maria Santos",
        "text": "My AC just died and it's 100 degrees in Miami. Called my usual guy but no one answers. Need help NOW or my kids will melt.",
        "niche": "HVAC"
    }
    
    print(f"🕵️ Radar detectando emergencia real: {live_case['author']}...")
    lead = scraper.process_review(live_case['author'], live_case['text'], live_case['niche'])
    
    if lead:
        print("💰 ¡LEAD DE ORO CONFIRMADO!")
        print(f"📝 Detección: {lead['summary']}")
        success = push_to_ghl(lead)
        if success:
            print("\n🚀 TEST FINALIZADO: El lead ya está en tu GHL.")
            print("👉 Si configuraste el Workflow, deberías recibir/ver el SMS de subasta con el link de pago.")

if __name__ == "__main__":
    run_live_test()
