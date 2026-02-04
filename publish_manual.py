import os
import sys
from deploy.linkedin_publisher import LinkedInPublisher
from dotenv import load_dotenv

load_dotenv()

def publish_latest():
    """
    Publica el último borrador generado si el usuario lo aprueba manualmente.
    """
    publisher = LinkedInPublisher()
    
    # Buscamos si hay un PDF listo para subir
    pdf_path = "autoridad_tecnica.pdf"
    if not os.path.exists(pdf_path):
        pdf_path = None
        
    print("📢 Preparando publicación manual...")
    
    # Intentamos leer el texto del último post generado (asumiendo que se guardó en algún log o archivo)
    # Por ahora, este script asume que el usuario quiere publicar lo que acaba de ver en Telegram.
    
    confirm = input("⚠️ ¿Estás SEGURO de que quieres publicar en LinkedIn ahora? (s/n): ")
    if confirm.lower() == 's':
        # Nota: En una versión más avanzada, leeríamos el texto exacto de un archivo 'last_draft.txt'
        print("🚀 Publicando...")
        # result = publisher.post_content(text, pdf_path=pdf_path)
        print("✅ Simulación: Publicación completada con éxito.")
    else:
        print("❌ Publicación cancelada.")

if __name__ == "__main__":
    publish_latest()
