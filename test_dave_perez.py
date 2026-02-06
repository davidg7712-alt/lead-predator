import os
import requests
import json
from dotenv import load_dotenv
from ghl_integration import push_to_ghl

load_dotenv()

def run_dave_perez_test():
    # Simulating the gold lead data for Dave Perez
    lead_data = {
        "author": "Dave Perez",
        "phone": "+16892330792",
        "text": "My AC is making a loud noise and stopped cooling. Need a technician in Miami immediately.",
        "summary": "Urgent HVAC emergency - No cooling in Miami heat.",
        "niche": "HVAC",
        "location": "Miami, FL",
        "lead_value": 69,
        "payment_link": "https://link.fastpaydirect.com/payment-link/6983a7006503ca57b583bbf5",
        "language": "EN"
    }
    
    print(f"🚀 Injecting Dave Perez (+16892330792) into GHL for Workflow Testing...")
    success = push_to_ghl(lead_data)
    
    if success:
        print("\n✅ Dave Perez pushed successfully!")
        print("👉 Check your GHL now. The 'Lead de Oro' tag should trigger your SMS within seconds.")
    else:
        print("\n❌ Failed to push Dave Perez.")

if __name__ == "__main__":
    run_dave_perez_test()
