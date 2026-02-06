import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

from intent_classifier import IntentClassifier
from apify_scraper import ApifyScraper
from skip_tracer import SkipTracer

class UniversalScraper:
    """
    The heart of the Lead Predator machine. 
    It scans different signals based on a modular configuration.
    Supports 'Broad Search' (Discovery) and 'Spy Mode' (High Frequency).
    """
    def __init__(self, config_path="niche_configs_production.json", spy_list_path="spy_list.json"):
        self.configs = self._load_configs(config_path)
        self.spy_list_path = spy_list_path
        self.classifier = IntentClassifier()
        self.apify = ApifyScraper()
        self.tracer = SkipTracer()
        
    def _load_configs(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def _load_spy_list(self):
        if os.path.exists(self.spy_list_path):
            try:
                with open(self.spy_list_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_to_spy_list(self, business_url):
        spy_list = self._load_spy_list()
        if business_url and business_url not in spy_list:
            spy_list.append(business_url)
            with open(self.spy_list_path, 'w') as f:
                json.dump(spy_list, f, indent=4)
            print(f"🕵️ Target añadido a la Lista de Espionaje: {business_url}")

    def process_review(self, author_name, review_text, niche_id, niche_config, business_url=None):
        """
        Uses AI to decide if this review is a gold lead.
        """
        classification_raw = self.classifier.classify_review(review_text, niche_config['niche'])
        try:
            classification = json.loads(classification_raw)
        except:
            return None
        
        if classification.get("tier") == "RED" and classification.get("is_lead"):
            # Si encontramos un Lead de Oro, este negocio es un buen target para espionaje futuro
            if business_url:
                self._save_to_spy_list(business_url)

            # Obtenemos el teléfono real si es posible
            phone = self.tracer.trace(author_name, niche_config['location'], niche_config['niche'])
            
            print(f"🔥 LEAD DE ORO DETECTADO: {author_name} ({phone})")
            return {
                "author": author_name,
                "phone": phone,
                "text": review_text,
                "tier": classification.get("tier"),
                "summary": classification.get("summary"),
                "niche": niche_config['niche'],
                "location": niche_config['location'],
                "lead_value": niche_config['lead_value'],
                "payment_link": niche_config['payment_link'],
                "language": classification.get("language", "EN")
            }
        return None

    def hunt(self, niche_name, mode="broad"):
        """
        Starts the hunt. 
        'broad' = Finds new businesses.
        'spy' = Monitors known bad-service businesses.
        """
        config = self.configs.get(niche_name)
        if not config:
            return []
            
        gold_leads = []
        
        if mode == "broad":
            print(f"📡 Radar AMPLIO para: {niche_name}...")
            query = f"{config['niche']} {config['location']}"
            raw_leads = self.apify.get_recent_negative_reviews(query)
        else:
            spy_list = self._load_spy_list()
            # Only spy on URLs relevant to this city/niche (simplified filter)
            relevant_urls = [url for url in spy_list if config['location'].split(',')[0].lower() in url.lower()]
            if not relevant_urls:
                return []
            print(f"🕵️ Radar QUIRÚRGICO para: {niche_name} ({len(relevant_urls)} targets)...")
            raw_leads = self.apify.get_reviews_by_urls(relevant_urls)

        for raw in raw_leads:
            gold_lead = self.process_review(raw['author'], raw['text'], niche_name, config)
            if gold_lead:
                gold_leads.append(gold_lead)
        
        return gold_leads

if __name__ == "__main__":
    scraper = UniversalScraper()
    # Initial Broad Hunt to populate spy list
    scraper.hunt("hialeah_hvac", mode="broad")
