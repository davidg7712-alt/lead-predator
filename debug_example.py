from deploy.ai_bot_prototype import AIConsentBot
import requests

def show_example():
    bot = AIConsentBot()
    
    print("--- 🔬 BUSCANDO UN PAPER REAL EN ARXIV ---")
    papers = bot.fetch_arxiv_papers(max_results=1)
    
    if papers:
        paper = papers[0]
        print(f"\n📄 Paper seleccionado: {paper['title']}")
        print(f"✍️ Autor: {paper['author']}")
        
        print("\n--- ✍️ GENERANDO POST (ESTILO CTO) ---")
        post = bot.generate_linkedin_post(paper)
        print("-" * 50)
        print(post)
        print("-" * 50)
        
        print("\n--- 🎨 GENERANDO IMAGEN CONTEXTUAL ---")
        print("(Diciéndole a la IA que incluya referencias reales al paper...)")
        image_url = bot.generate_image(paper)
        
        print(f"\n✅ IMAGEN GENERADA: {image_url}")
        
        # Guardamos el ejemplo en un archivo para el usuario
        with open("ejemplo_autoridad.md", "w", encoding="utf-8") as f:
            f.write(f"# 🧪 Ejemplo de Post de Autoridad (ArXiv)\n\n")
            f.write(f"## 📄 Paper Original: {paper['title']}\n")
            f.write(f"**Abstract:** {paper['description'][:300]}...\n\n")
            f.write(f"## 🖼️ Imagen Contextual (Mockup del Bot)\n![Ejemplo de imagen]({image_url})\n\n")
            f.write(f"## ✍️ Texto del Post (Vino del Ghostwriter CTO)\n\n---\n\n{post}\n\n---\n")

if __name__ == "__main__":
    show_example()
