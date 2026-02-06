import os
import requests
from dotenv import load_dotenv

load_dotenv()

def inject_test_tags():
    api_key = os.getenv("GHL_API_KEY", "").strip()
    location_id = os.getenv("GHL_LOCATION_ID", "").strip()
    
    contacts = [
        {"name": "Test Spanish", "tag": "Lang: ES", "phone": "+10000000001"},
        {"name": "Test English", "tag": "Lang: EN", "phone": "+10000000002"}
    ]
    
    url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    for c in contacts:
        payload = {
            "firstName": c["name"],
            "phone": c["phone"],
            "locationId": location_id,
            "tags": ["Lead de Oro", c["tag"]]
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                print(f"✅ Tag '{c['tag']}' creado con éxito en GHL.")
            else:
                print(f"❌ Error creando tag '{c['tag']}': {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_test_tags()
