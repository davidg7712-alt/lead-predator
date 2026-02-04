import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

from intent_classifier import IntentClassifier
from apify_scraper import ApifyScraper

class UniversalScraper:
    """
    The heart of the Lead Predator machine. 
    It scans different signals based on a modular configuration.
    """
    def __init__(self, config_path="niche_configs.json"):
        self.configs = self._load_configs(config_path)
        self.classifier = IntentClassifier()
        self.apify = ApifyScraper()
        
    def _load_configs(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    def process_review(self, author_name, review_text, niche_id, niche_config):
        """
        Uses AI to decide if this review is a gold lead.
        """
        classification = json.loads(self.classifier.classify_review(review_text, niche_config['niche']))
        
        if classification.get("tier") == "RED" and classification.get("is_lead"):
            print(f"🔥 LEAD DE ORO DETECTADO: {author_name}")
            return {
                "author": author_name,
                "text": review_text,
                "tier": classification.get("tier"),
                "summary": classification.get("summary"),
                "niche": niche_config['niche'],
                "lead_value": niche_config['lead_value'],
                "payment_link": niche_config['payment_link']
            }
        return None

    def hunt(self, niche_name):
        """
        Starts the hunt for a specific niche using Apify.
        """
        config = self.configs.get(niche_name)
        if not config:
            print(f"❌ Niche '{niche_name}' not configured.")
            return []
            
        print(f"📡 Radar iniciado para: {niche_name} en {config['location']}...")
        
        # 1. Scrape Google Maps via Apify
        query = f"{config['niche']} {config['location']}"
        raw_leads = self.apify.get_recent_negative_reviews(query)
        
        gold_leads = []
        for raw in raw_leads:
            print(f"🧐 Analizando reseña de {raw['author']} en {raw['business']}...")
            gold_lead = self.process_review(raw['author'], raw['text'], niche_name, config)
            if gold_lead:
                gold_leads.append(gold_lead)
        
        return gold_leads

if __name__ == "__main__":
    # Test initialization
    scraper = UniversalScraper()
    scraper.hunt("miami_hvac")
