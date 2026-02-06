import os
import json
import time
import requests
from dotenv import load_dotenv
from UniversalScraper import UniversalScraper

load_dotenv()

class LeadPredatorProduction:
    """
    Production loop for the Lead Predator.
    Targets high-friction cities and emergency niches.
    """
    def __init__(self, config_path="niche_configs_production.json"):
        self.scraper = UniversalScraper(config_path=config_path)
        self.api_key = os.getenv("GHL_API_KEY")
        self.location_id = os.getenv("GHL_LOCATION_ID")
        
    def push_to_ghl(self, lead_data):
        """
        Pushes a verified gold lead to GoHighLevel.
        """
        url = "https://rest.gohighlevel.com/v1/contacts/"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Prepare payload with prioritized information
        payload = {
            "firstName": lead_data['author'].split()[0],
            "lastName": lead_data['author'].split()[-1] if len(lead_data['author'].split()) > 1 else "",
            "phone": lead_data.get('phone') or "+10000000000", # Fallback if skip tracing failed
            "locationId": self.location_id,
            "tags": ["Lead de Oro", f"{lead_data['niche']} {lead_data['location']}", "Active Emergency"],
            "customField": {
                "intent_summary": lead_data['summary'],
                "original_review": lead_data['text'],
                "lead_value": lead_data['lead_value'],
                "payment_link": lead_data['payment_link']
            }
        }

        try:
            print(f"📤 Inyectando lead de {lead_data['author']} en GHL...")
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                print(f"✅ ÉXITO: Lead inyectado para subasta.")
                return True
            else:
                print(f"⚠️ Error GHL ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error en conexión GHL: {e}")
            return False

    def run_full_scan(self):
        """
        Runs one full scan cycle across all configured niches.
        """
        print("\n" + "="*50)
        print(f"🚀 INICIANDO CICLO DE CACERÍA: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
        
        all_configs = self.scraper.configs
        total_leads_found = 0
        
        for niche_name in all_configs.keys():
            try:
                # 1. Start the hunt
                gold_leads = self.scraper.hunt(niche_name)
                
                # 2. Process findings
                for lead in gold_leads:
                    print(f"💰 ¡ORO ENCONTRADO! {lead['author']} necesita {lead['niche']} en {lead['location']}")
                    if self.push_to_ghl(lead):
                        total_leads_found += 1
                
                # 3. Polite pause between cities to avoid rate limits
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Error escaneando nicho {niche_name}: {e}")
                continue
                
        print("\n" + "="*50)
        print(f"🏁 CICLO COMPLETADO. Leads totales inyectados hoy: {total_leads_found}")
        print("="*50 + "\n")

if __name__ == "__main__":
    hunter = LeadPredatorProduction()
    hunter.run_full_scan()
