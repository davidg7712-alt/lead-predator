import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_ghl_connection():
    api_key = os.getenv("GHL_API_KEY")
    location_id = os.getenv("GHL_LOCATION_ID")
    
    if not api_key or not location_id:
        print("❌ Error: GHL_API_KEY or GHL_LOCATION_ID missing in .env")
        return

    # GHL V1 API endpoint for testing
    url = f"https://rest.gohighlevel.com/v1/locations/{location_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("✅ Conexión con GoHighLevel exitosa!")
            print(f"📍 Location Branch: {response.json().get('location', {}).get('name')}")
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_ghl_connection()
