import os
import json
from UniversalScraper import UniversalScraper
from dotenv import load_dotenv

load_dotenv()

def start_real_hunt():
    """
    Triggers the Lead Predator machine to find REAL world leads using Apify.
    """
    scraper = UniversalScraper()
    
    print("🚀 LANZANDO EL PREDADOR EN VIVO (MIAMI HVAC)...")
    print("⏳ Esto puede tardar unos 60-90 segundos mientras Apify escanea Google Maps...")
    
    # We hunt in the 'miami_hvac' niche defined in niche_configs.json
    gold_leads = scraper.hunt("miami_hvac")
    
    if not gold_leads:
        print("\nℹ️ El radar no ha encontrado emergencias críticas de 1-2 estrellas en las últimas 24h.")
        print("💡 Esto es normal en nichos pequeños. El bot seguirá escaneando cada X minutos.")
    else:
        print(f"\n💰 ¡ÉXITO! Se han encontrado {len(gold_leads)} leads de ORO reales.")
        for i, lead in enumerate(gold_leads):
            print(f"\n--- Lead #{i+1} ---")
            print(f"👤 Cliente: {lead['author']}")
            print(f"📝 Problema: {lead['text'][:100]}...")
            print(f"🔍 Análisis IA: {lead['summary']}")
            # In a real scenario, we would now push to GHL
            # push_to_ghl(lead)

if __name__ == "__main__":
    start_real_hunt()
