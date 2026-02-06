import os
import json
from datetime import datetime, timedelta
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

class ApifyScraper:
    """
    Scrapes Google Maps reviews using the web_wanderer/google-reviews-scraper actor.
    Supports both broad searching and specific business monitoring (Spy Mode).
    """
    def __init__(self):
        self.api_token = os.getenv("APIFY_API_TOKEN", "").strip()
        self.client = ApifyClient(self.api_token)

    def get_recent_negative_reviews(self, search_query, limit=10):
        """
        Broad Search: Finds businesses in a city and looks for negative reviews.
        """
        print(f"🔍 Buscando negocios en Apify para: {search_query}")
        parts = search_query.split(" ", 1)
        search_term = parts[0]
        location = parts[1] if len(parts) > 1 else ""

        run_input = {
            "search": [search_term],
            "search_location": location,
            "order": "newest",
            "limit": limit,
            "rating": "0.0",
            "lang": "en",
            "include_personal": True,
            "source": "google"
        }

        try:
            print(f"📡 Lanzando actor: web_wanderer/google-reviews-scraper...")
            run = self.client.actor("web_wanderer/google-reviews-scraper").call(run_input=run_input, timeout_secs=180)
            return self._process_items(run["defaultDatasetId"])
        except Exception as e:
            print(f"❌ Error en Apify (Broad): {e}")
            return []

    def get_reviews_by_urls(self, urls, limit_per_place=2):
        """
        Spy Mode: Specifically monitors a list of businesses (URLs).
        Ultra-efficient and low-latency.
        """
        print(f"🕵️ MODO ESPÍA ACTIVADO: Monitoreando {len(urls)} negocios específicos...")
        run_input = {
            "start_urls": [{"url": url} for url in urls],
            "order": "newest",
            "limit": limit_per_place,
            "rating": "0.0",
            "lang": "en",
            "include_personal": True,
            "source": "google"
        }

        try:
            print(f"📡 Lanzando actor quirúrgico: web_wanderer/google-reviews-scraper...")
            run = self.client.actor("web_wanderer/google-reviews-scraper").call(run_input=run_input, timeout_secs=180)
            return self._process_items(run["defaultDatasetId"])
        except Exception as e:
            print(f"❌ Error en Modo Espía: {e}")
            return []

    def _process_items(self, dataset_id):
        leads = []
        for item in self.client.dataset(dataset_id).iterate_items():
            stars = item.get("rating")
            if stars and stars <= 2:
                leads.append({
                    "business": item.get("place_name") or "Unknown Business",
                    "author": item.get("reviewer_name") or "Anonymous",
                    "text": item.get("text"),
                    "rating": stars,
                    "published_at": item.get("published_at") or item.get("date")
                })
        return leads

if __name__ == "__main__":
    scraper = ApifyScraper()
    # Test search
    # results = scraper.get_recent_negative_reviews("HVAC Miami, FL")
    # print(json.dumps(results, indent=2))
