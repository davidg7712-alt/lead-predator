import time
import os
import schedule
from datetime import datetime
from UniversalScraper import UniversalScraper
from ghl_integration import push_to_ghl
from dotenv import load_dotenv

load_dotenv()

def job():
    print(f"\n🚀 [Predator] Iniciando ronda de escaneo a las {datetime.now().strftime('%H:%M:%S')}...")
    scraper = UniversalScraper()
    
    # Recorremos todos los nichos configurados
    for niche_id, config in scraper.configs.items():
        # Verificación de horarios de oficina (Simple check)
        now_hour = datetime.now().hour
        start_hour = int(config['operating_hours']['start'].split(':')[0])
        end_hour = int(config['operating_hours']['end'].split(':')[0])
        
        if not (start_hour <= now_hour < end_hour):
            print(f"💤 {niche_id} está fuera de horario operativo ({config['operating_hours']['start']} - {config['operating_hours']['end']}). Saltando...")
            continue
            
        print(f"📡 Escaneando {niche_id}...")
        gold_leads = scraper.hunt(niche_id)
        
        for lead in gold_leads:
            print(f"💰 ¡LEAD DE ORO DETECTADO! ({lead['author']}) - Inyectando en GHL...")
            push_to_ghl(lead)
            # Sleep pequeño para evitar spam en la API de GHL
            time.sleep(2)

def start_scheduler():
    print("🤖 El Predador está en modo 'Siempre Encendido'.")
    print("⏱️ Configurado para buscar cada 30 minutos.")
    
    # Programamos la tarea cada 30 minutos
    schedule.every(30).minutes.do(job)
    
    # Ejecución inicial
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Necesitaremos instalar la librería schedule: pip install schedule
    start_scheduler()
