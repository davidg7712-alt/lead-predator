import os
import json
from datetime import datetime, timedelta
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

class ApifyScraper:
    """
    Scrapes Google Maps reviews using the web_wanderer/google-reviews-scraper actor found in the user's account.
    """
    def __init__(self):
        self.api_token = os.getenv("APIFY_API_TOKEN")
        self.client = ApifyClient(self.api_token)

    def get_recent_negative_reviews(self, search_query, limit=10):
        """
        Searches for negative reviews using the web_wanderer actor.
        """
        print(f"🔍 Buscando negocios en Apify para: {search_query}")
        
        # Split search query into term and location for the web_wanderer actor
        # Example: "HVAC Miami, FL" -> search=["HVAC"], location="Miami, FL"
        parts = search_query.split(" ", 1)
        search_term = parts[0]
        location = parts[1] if len(parts) > 1 else ""

        run_input = {
            "search": [search_term],
            "search_location": location,
            "order": "newest",
            "limit": limit,
            "rating": "0.0", # Fetch all and filter in Python to be precise
            "lang": "en",
            "include_personal": True,
            "source": "google"
        }

        try:
            print(f"📡 Lanzando actor: web_wanderer/google-reviews-scraper...")
            run = self.client.actor("web_wanderer/google-reviews-scraper").call(run_input=run_input, timeout_secs=180)
            
            leads = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                # Corrected keys for web_wanderer output
                stars = item.get("rating")
                if stars and stars <= 2:
                    leads.append({
                        "business": item.get("place_name") or "Unknown Business",
                        "author": item.get("reviewer_name") or "Anonymous",
                        "text": item.get("text"),
                        "rating": stars,
                        "published_at": item.get("published_at") or item.get("date")
                    })
            
            if leads:
                print(f"✅ Se encontraron {len(leads)} posibles leads de 1-2 estrellas.")
            return leads
        except Exception as e:
            print(f"❌ Error en Apify: {e}")
            return []

if __name__ == "__main__":
    scraper = ApifyScraper()
    # Test search
    results = scraper.get_recent_negative_reviews("HVAC Miami, FL")
    print(json.dumps(results, indent=2))
