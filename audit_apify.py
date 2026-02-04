import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def audit_apify():
    client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
    
    print("📋 Revisando Actores en 'Mis Actores'...")
    try:
        my_actors = client.actors().list()
        for actor in my_actors.items:
            print(f"- {actor['username']}/{actor['name']} (ID: {actor['id']})")
    except Exception as e:
        print(f"❌ Error listando mis actores: {e}")

    print("\n🕒 Revisando Historial de Ejecuciones (Runs)...")
    try:
        runs = client.runs().list(limit=10)
        for run in runs.items:
            # Get actor name from actorId if possible
            try:
                actor = client.actor(run['actorId']).get()
                actor_name = f"{actor['username']}/{actor['name']}"
            except:
                actor_name = run['actorId']
                
            print(f"- {actor_name} | Status: {run['status']} | Iniciado: {run['startedAt']}")
    except Exception as e:
        print(f"❌ Error listando ejecuciones: {e}")

if __name__ == "__main__":
    audit_apify()
