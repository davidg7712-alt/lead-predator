import time
import os
import schedule
import pytz
from datetime import datetime
from UniversalScraper import UniversalScraper
from ghl_integration import push_to_ghl
from dotenv import load_dotenv

load_dotenv()

def job():
    scraper = UniversalScraper()
    print(f"\n🚀 [Predador] Iniciando ronda de escaneo global...")
    
    # Recorremos todos los nichos configurados
    for niche_id, config in scraper.configs.items():
        # Verificación de horarios de oficina con Timezone
        timezone_str = config['operating_hours'].get('timezone', 'America/New_York')
        tz = pytz.timezone(timezone_str)
        now_local = datetime.now(tz)
        
        now_hour = now_local.hour
        start_hour = int(config['operating_hours']['start'].split(':')[0])
        end_hour = int(config['operating_hours']['end'].split(':')[0])
        
        if not (start_hour <= now_hour < end_hour):
            print(f"💤 {niche_id} está fuera de horario ({config['operating_hours']['start']} - {config['operating_hours']['end']} {timezone_str}). Hora actual: {now_local.strftime('%H:%M')}")
            continue
            
        print(f"📡 Radar activo: {niche_id}...")
        gold_leads = scraper.hunt(niche_id)
        
        for lead in gold_leads:
            print(f"💰 ¡LEAD DE ORO! Enyectando '{lead['author']}' en GHL...")
            push_to_ghl(lead)
            time.sleep(2)

def start_scheduler():
    print("🤖 El Predador está ONLINE.")
    print("⏱️ Configurado para buscar cada 30 minutos.")
    
    # Programamos la tarea cada 30 minutos
    schedule.every(30).minutes.do(job)
    
    # Ejecución inicial
    job()
    
    while True:
        schedule.run_pending()
        # Heartbeat para evitar que Railway piense que estamos muertos
        if datetime.now().minute % 10 == 0:
            print(f"💓 Heartbeat: Bot activo a las {datetime.now().strftime('%H:%M')} (UTC)")
        time.sleep(60)

if __name__ == "__main__":
    start_scheduler()
