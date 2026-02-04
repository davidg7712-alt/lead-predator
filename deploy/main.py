import time
import requests
from ai_bot_prototype import AIConsentBot
from telegram_approver import TelegramApprover
from linkedin_publisher import LinkedInPublisher
import os
from dotenv import load_dotenv

load_dotenv()

def run_bot(publish=False):
    bot = AIConsentBot()
    approver = TelegramApprover()
    publisher = LinkedInPublisher()

    print(f"🛡️ MODO {'PRODUCCIÓN' if publish else 'SEGURIDAD'} ACTIVO")
    
    # 1. Contenido de Alta Autoridad (Escaneo Diversificado)
    papers = bot.fetch_arxiv_papers(query="cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.RO", max_results=20)
    if not papers: return
    article = papers[0]
    
    # 2. Análisis y Hacks
    post_text = bot.generate_linkedin_post(article)
    growth_hacks = bot.get_growth_hacks(article)
    slide_content = bot.generate_slide_content(article)
    
    # 3. Carrusel Tipográfico
    image_paths = []
    for i in range(1, 4):
        path = bot.generate_image(article, slide_num=i, total_slides=3, slide_content=slide_content)
        image_paths.append(path)
    
    pdf_path = bot.create_pdf_from_images(image_paths, "autoridad_comunidad.pdf")
    
    if publish:
        print("🚀 PUBLICANDO EN LINKEDIN...")
        result = publisher.post_content(post_text, pdf_path=pdf_path, title=article['title'])
        
        if "SUCCESS" in result:
            import time
            post_urn = result.split(":")[1]
            print(f"✅ Post published: {post_urn}")
            
            # --- HACK DE ÉLITE: AUTO-TAGGING EN COMENTARIO ---
            print("⏳ Waiting 10 seconds for LinkedIn to index the post...")
            time.sleep(10) 
            
            print("💬 Publishing automated English comment with author tagging...")
            author_tag = article.get('author', 'the research team')
            comment_text = f"Exceptional research on this paper. @{author_tag}, how do you see this framework impacting mid-market operational costs? \n\nPD: Comment 'CORE' or 'MAPA' for the full technical breakdown. 👇"
            
            comment_success = publisher.post_comment(post_urn, comment_text, author_name=author_tag)
            if comment_success:
                print("✅ Global authority comment published successfully.")
            else:
                print(f"⚠️ Warning: Auto-comment failed for {post_urn}. Check API permissions or Rate Limits.")
        else:
            print(f"❌ Error en publicación: {result}")
    else:
        # Modo Propuesta
        status_msg = f"🏆 **PROPUESTA PARA REVISAR**\n\n{post_text}\n\n{growth_hacks}\n\n📊 **ESTADO:** Solo propuesta. Nada publicado."
        approver.send_proposal(status_msg, image_paths=image_paths)
        print("📲 Propuesta enviada a Telegram.")

if __name__ == "__main__":
    import sys
    # Si se pasa el argumento --publish, se publica de verdad
    publish_now = "--publish" in sys.argv
    run_bot(publish=publish_now)
