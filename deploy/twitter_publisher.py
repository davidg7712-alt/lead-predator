import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class TwitterPublisher:
    def __init__(self, api_key=None, api_secret=None, access_token=None, access_token_secret=None):
        self.api_key = api_key or os.getenv("TWITTER_API_KEY")
        self.api_secret = api_secret or os.getenv("TWITTER_API_SECRET")
        self.access_token = access_token or os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        # Cliente para la API v2 (Para postear texto)
        self.client = tweepy.Client(
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
        
        # Auth para la API v1.1 (Para subir imágenes)
        auth = tweepy.OAuth1UserHandler(
            self.api_key, self.api_secret, self.access_token, self.access_token_secret
        )
        self.api_v1 = tweepy.API(auth)

    def post_tweet(self, text, image_path=None):
        """
        Publica un tweet, opcionalmente con una imagen.
        """
        try:
            if image_path and os.path.exists(image_path):
                # Paso 1: Subir imagen vía v1.1
                media = self.api_v1.media_upload(filename=image_path)
                media_id = media.media_id
                
                # Paso 2: Publicar Tweet con la imagen vía v2
                response = self.client.create_tweet(text=text, media_ids=[media_id])
            else:
                response = self.client.create_tweet(text=text)
            
            return f"Tweet publicado exitosamente. ID: {response.data['id']}"
        except Exception as e:
            return f"Error al publicar en Twitter: {e}"

if __name__ == "__main__":
    # Test (requiere llaves)
    publisher = TwitterPublisher()
    # print(publisher.post_tweet("¡Hola Twitter! Este es mi primer post automático desde mi bot de IA."))
