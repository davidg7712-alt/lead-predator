import tweepy
import os

# Credenciales finales proporcionadas por David
API_KEY = "dQCc8Gn7hGVvLObBFHpsX4epS"
API_SECRET = "ed8Af6WfKrKH9xtprgUesc7DtgpalHydhU1ZadmOWpDpJJPD0L"
ACCESS_TOKEN = "347272654-4JBgQzmKce07FQLDRGZKASTawNPAhxQD1i5f69E1"
ACCESS_SECRET = "l3i55dYwZ1sbysONDElug7qtkcFJH6df6AGJTtnoMCQez"

def test_live_post():
    print("🚀 Iniciando prueba de fuego en Twitter...")
    try:
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET
        )
        response = client.create_tweet(text="🚀 Probando mi nuevo bot de IA bilingüe. ¡Hola mundo! #AI #Automation")
        print(f"✅ ¡ÉXITO! Tweet publicado con ID: {response.data['id']}")
        print("🔗 Verifica tu perfil de Twitter ahora mismo.")
    except Exception as e:
        print(f"❌ ERROR: Los tokens no tienen permiso de escritura o son inválidos: {e}")

if __name__ == "__main__":
    test_live_post()
