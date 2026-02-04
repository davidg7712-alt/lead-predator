import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramApprover:
    def __init__(self, token=None, chat_id=None):
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        
    def send_proposal(self, text, image_paths=None):
        """
        Sends the post proposal to Telegram for approval.
        """
        if not self.token or not self.chat_id:
            return "Error: Telegram credentials missing."
            
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🤖 **Nueva Propuesta (Modo Estratégico)**\n\n{text}\n\n¿Publicar? (Responde 'SI' para autorizar)",
            "parse_mode": "Markdown"
        }
        
        # Enviar texto
        requests.post(url, json=payload)
        
        # Enviar carrusel si existen imágenes
        if image_paths:
            for path in image_paths:
                if os.path.exists(path):
                    img_url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
                    with open(path, 'rb') as photo:
                        requests.post(img_url, data={'chat_id': self.chat_id}, files={'photo': photo})
        
        return "Propuesta enviada a Telegram."

if __name__ == "__main__":
    # Test (necesita las keys en .env)
    approver = TelegramApprover()
    print(approver.send_proposal("Este es un post de prueba para LinkedIn... #IA #Test"))
