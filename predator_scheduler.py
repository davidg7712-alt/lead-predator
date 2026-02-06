import time
import os
import schedule
import pytz
import json
from datetime import datetime
from UniversalScraper import UniversalScraper
from ghl_integration import push_to_ghl
from dotenv import load_dotenv

load_dotenv()

def get_spy_list_size():
    path = "spy_list.json"
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return len(json.load(f))
        except:
            return 0
    return 0

def cycle_job(niche_id, mode="spy"):
    scraper = UniversalScraper(config_path="niche_configs_production.json")
    config = scraper.configs.get(niche_id)
    if not config: return

    # Check Operating Hours
    timezone_str = config['operating_hours'].get('timezone', 'America/New_York')
    tz = pytz.timezone(timezone_str)
    now_local = datetime.now(tz)
    
    now_hour = now_local.hour
    start_hour = int(config['operating_hours']['start'].split(':')[0])
    end_hour = int(config['operating_hours']['end'].split(':')[0])
    
    if not (start_hour <= now_hour < end_hour):
        return
        
    print(f"📡 [{mode.upper()} - {niche_id}] Hunter activo...")
    gold_leads = scraper.hunt(niche_id, mode=mode)
    
    for lead in gold_leads:
        print(f"💰 ¡LEAD DE ORO! Inyectando '{lead['author']}' en GHL...")
        push_to_ghl(lead)
        time.sleep(2)

def job_wrapper_speed(scraper_instance):
    # This function will be called every 15 minutes
    # It should iterate through all niches and run cycle_job in "spy" mode
    for niche_id in scraper_instance.configs.keys():
        cycle_job(niche_id, mode="spy")

def job_wrapper_discovery(scraper_instance):
    # This function will be called twice a day
    # It should iterate through all niches and run cycle_job in "broad" mode
    for niche_id in scraper_instance.configs.keys():
        cycle_job(niche_id, mode="broad")

def start_scheduler():
    load_dotenv()
    print("\n" + "="*50)
    print("🤖 EL PREDADOR ESTÁ ONLINE (TURBO-LEARNING ENABLED)")
    print("="*50 + "\n")
    
    # --- PLAN ESTÁNDAR GOLPE DE VELOCIDAD (ZERO-LATENCY) ---
    # Costo Apify: $0.35 x 1000 reviews. Con $49/mes, tenemos 140,000 reviews.
    # Estrategia: Frecuencia EXTREMA (15 min) en Horario Laboral (9AM-6PM) para Spy Mode.
    # El Radar Amplio (Broad) solo 2 veces al día para no quemar el presupuesto.
    
    spy_size = get_spy_list_size()
    print(f"⚡ [Modo Sniper] Spy List: {spy_size} targets | Plan Estándar OK")
    
    scraper = UniversalScraper(config_path="niche_configs_production.json")
    
    # 1. MODO ESPÍA (ALTA VELOCIDAD)
    # Corre CADA 15 MINUTOS. Es barato y detecta el lead al segundo de ser posteado.
    schedule.every(15).minutes.do(job_wrapper_speed, scraper)
    
    # 2. MODO DISCOVERY (BARRIDO AMPLIO)
    # Solo 2 veces al día (Madrugada y Mediodía) para meter sangre nueva a la lista de espionaje.
    schedule.every().day.at("04:00").do(job_wrapper_discovery, scraper)
    schedule.every().day.at("13:00").do(job_wrapper_discovery, scraper)
    
    print("⏰ Horario Florida (9AM-6PM) -> Escaneo cada 15 min")
    print("⏰discovery -> 04:00 AM y 01:00 PM")
    
    # Primera ejecución controlada
    print("\n🚀 Ejecutando barrido inicial...")
    for niche_id in scraper.configs.keys():
        cycle_job(niche_id, mode="spy") # Solo el barato primero
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
