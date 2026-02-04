import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def list_apify_actors():
    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
    print("📋 Listando actores disponibles en tu cuenta de Apify...")
    try:
        # We can't easily list "Store" actors they haven't added,
        # but we can try to see if they have any 'my-actors' or if we can find the most common public one.
        # Actually, let's try to call 'apify/google-maps-scraper' which is the most common one.
        actors = client.actors().list()
        for actor in actors.items:
            print(f"- {actor['username']}/{actor['name']} ({actor['id']})")
        
        if not actors.items:
            print("ℹ️ No tienes actores propios. Intentaremos usar uno público de la Store.")
    except Exception as e:
        print(f"❌ Error listando actores: {e}")

if __name__ == "__main__":
    list_apify_actors()
