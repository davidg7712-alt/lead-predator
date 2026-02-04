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
    
    # We simulate a phone number for the lead (in real case search_tracer finds it)
    payload = {
        "firstName": lead_data['author'].split()[0],
        "lastName": lead_data['author'].split()[-1] if len(lead_data['author'].split()) > 1 else "",
        "phone": "+17865550199", # Demo Phone
        "locationId": location_id,
        "tags": ["Lead de Oro", "Miami HVAC", "Active Emergency"],
        "customField": {
            "intent_summary": lead_data['summary'],
            "original_review": lead_data['text']
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Lead '{lead_data['author']}' inyectado con éxito en GHL.")
            return True
        else:
            print(f"❌ Error inyectando lead: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Error GHL: {e}")
        return False

def run_demo_cycle():
    scraper = UniversalScraper()
    
    # Simulating a Red-Tier Lead found in Miami
    demo_review = {
        "author": "Juan Rodriguez",
        "text": "The technician from MiamiAC never showed up. It's 95 degrees inside and I have kids. Unacceptable service.",
        "niche": "HVAC"
    }
    
    print(f"🕵️ Detectando posible lead: {demo_review['author']}...")
    lead = scraper.process_review(demo_review['author'], demo_review['text'], demo_review['niche'])
    
    if lead:
        print("💰 Procesando Lead de Oro para subasta...")
        success = push_to_ghl(lead)
        if success:
            print("🚀 El sistema de GHL disparará ahora el SMS de subasta a los contratistas.")

if __name__ == "__main__":
    run_demo_cycle()
