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

def start_scheduler():
    load_dotenv()
    print("\n" + "="*50)
    print("🤖 EL PREDADOR ESTÁ ONLINE (TURBO-LEARNING ENABLED)")
    print("="*50 + "\n")
    
    # --- ESTRATEGIA DE AHORRO DE CRÉDITOS (PLAN SNIPER) ---
    # 1. El Radar Amplio (Discovery) es caro, lo bajamos a 6 horas para todos.
    # 2. El Radar Quirúrgico (Spy) es barato, lo mantenemos cada 45 min.
    
    spy_size = get_spy_list_size()
    print(f"🔭 Configurando Predador (Spy List: {spy_size} objetivos)")
    
    scraper = UniversalScraper(config_path="niche_configs_production.json")
    
    for niche_id in scraper.configs.keys():
        config = scraper.configs[niche_id]
        
        # Modo Espía: Rápido y barato (45 min)
        schedule.every(45).minutes.do(cycle_job, niche_id, mode="spy")
        
        # Modo Discovery: Lento y caro (Cada 6 horas o según nicho crítico)
        # Si el nicho es 'High Friction', lo dejamos en 3 horas. Si no, 6 horas.
        is_critical = config.get('priority') == "High Friction"
        freq_mins = 180 if is_critical else 360 
        
        print(f"⏰ {niche_id}: Spy(45m) | Broad({freq_mins}m)")
        schedule.every(freq_mins).minutes.do(cycle_job, niche_id, mode="broad")
    
    # Primera ejecución controlada
    print("\n🚀 Ejecutando barrido inicial...")
    for niche_id in scraper.configs.keys():
        cycle_job(niche_id, mode="spy") # Solo el barato primero
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
