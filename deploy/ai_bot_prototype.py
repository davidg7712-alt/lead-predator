import os
import requests
from datetime import datetime, timedelta
import json
import random
import arxiv
from dotenv import load_dotenv
from openai import OpenAI
try:
    from visual_engine import CarouselGenerator
except ImportError:
    from .visual_engine import CarouselGenerator

load_dotenv()

class AIConsentBot:
    def __init__(self, news_api_key=None, openai_api_key=None):
        self.news_api_key = news_api_key or os.getenv("NEWS_API_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
        self.headers = {'User-agent': 'AIConsentBot 1.0'}
        
    def fetch_top_ai_news(self, language='en', page_size=5):
        """
        Fetches top AI news from the last 24 hours.
        Defaulted to English for Global Authority.
        """
        if not self.news_api_key:
            return "Error: NEWS_API_KEY not found."
            
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q=artificial intelligence OR IA OR AI&"
            f"from={yesterday}&"
            f"sortBy=popularity&"
            f"language={language}&"
            f"pageSize={page_size}&"
            f"apiKey={self.news_api_key}"
        )
        
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return articles
        else:
            return f"Error fetching news: {response.status_code}"

    def fetch_arxiv_papers(self, query="cat:cs.AI OR cat:cs.LG OR cat:cs.CV OR cat:cs.RO", max_results=20):
        """
        Radically expanded and filtered search.
        """
        print(f"🔬 Escaneando el horizonte tecnológico ({query})...")
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        papers_list = []
        blacklist_authors = ["Peter Chen", "Peter L. Chen", "Peter Lau-Luk Chen"]
        
        client = arxiv.Client()
        for result in client.results(search):
            # Check ALL authors, not just the first one
            all_author_names = [a.name for a in result.authors]
            is_blacklisted = any(any(blacklisted in name for name in all_author_names) for blacklisted in blacklist_authors)
            
            if not is_blacklisted:
                papers_list.append({
                    'title': result.title,
                    'url': result.pdf_url,
                    'description': result.summary,
                    'published': result.published.strftime('%Y-%m-%d'),
                    'author': result.authors[0].name if result.authors else "Scientific Team"
                })
        
        if not papers_list: 
            print("⚠️ Todos los papers recientes ya han sido filtrados o no hay nuevos.")
            return []
            
        # Retornamos uno aleatorio del pool de 20 para máxima variedad diaria
        return [random.choice(papers_list)]

    def generate_slide_content(self, article):
        """
        Generates rich, multi-point content in ENGLISH for the slides.
        Each slide gets 2-3 points to fill the space.
        """
        if not self.openai_api_key:
            return [["Detail 1"], ["Detail 2"], ["Detail 3"]]
            
        client = OpenAI(api_key=self.openai_api_key)
        prompt = f"""
        Article: {article['title']}
        Summary: {article.get('description', '')}
        
        TASK: Create high-authority content for 3 slides in ENGLISH.
        Guidelines:
        - Slide 1: THE DISRUPTION (2-3 bullets on why current systems fail).
        - Slide 2: THE "GENIUS" SHIFT (2-3 bullets on the core technical secret).
        - Slide 3: THE OPERATIONAL EDGE (2-3 bullets on ROI and industry impact).
        - LENGTH: Each bullet must be 40-70 characters. Fill the slide.
        - Tone: Strategic, High-Authority.
        - LANGUAGE: 100% ENGLISH.
        - Format: JSON list of lists [ [slide1_pts], [slide2_pts], [slide3_pts] ]
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            # Intentar parsear el JSON retornado
            data = json.loads(response.choices[0].message.content)
            # Buscamos la primera lista de listas que encontremos
            for key in data:
                if isinstance(data[key], list):
                    return data[key][:3]
            return [["Technical Challenge"], ["Innovative Approach"], ["Market Impact"]]
        except:
            return [[article['title'][:50]], ["System overview"], ["Global impact"]]

    def generate_image(self, context, slide_num=1, total_slides=3, slide_content=None):
        """
        Phase 11: International Authority Graphic Engine.
        Uses rich bullet points to fill the space.
        """
        visual = CarouselGenerator()
        
        # Headers in English
        headers = ["THE CHALLENGE", "THE SOLUTION", "MARKET IMPACT"]
        
        points = slide_content[slide_num - 1] if slide_content and len(slide_content) >= slide_num else ["Analyzing data..."]
            
        return visual.create_slide(headers[slide_num-1], points, slide_num, total_slides)

    def generate_linkedin_post(self, article, language='en'):
        """
        Phase 21: High-Stakes Business Strategy Lead.
        Focuses on profit, market position, and 'Common Sense' ROI.
        """
        if not self.openai_api_key:
            return "Error: OPENAI_API_KEY not found."
            
        client = OpenAI(api_key=self.openai_api_key)
        
        prompt = f"""
        Act as a High-Level Strategy Consultant (ex-McKinsey/Venture Capitalist). 
        Your goal is to explain a complex AI paper in terms of BUSINESS OPPORTUNITY and PROFIT.
        
        TOPIC: {article['title']}
        SUMMARY: {article.get('description', '')}
        
        WRITING GUIDELINES (MANDATORY):
        1. **NO JARGON**: No academic terms. Talk about "market leverage", "competitive moats", and "roi".
        2. **THE 'WHY SHOULD I CARE?'**: Start with a hook about market competition. "The industry is overcomplicating X, while the smart money is moving to Y."
        3. **THE THREE PILLARS**: Break the technical paper into 3 simple strategic takeaways:
           - Pillar 1: Cost reduction/Profit increase.
           - Pillar 2: Faster implementation.
           - Pillar 3: Reducing risk/Model stability.
        4. **HUMAN TONE**: Write like a senior partner at a firm. Cold, calculated, but readable. Zero emojis. Lots of whitespace.
        5. **BILINGUAL STRATEGY**: Ensure the Spanish section is a 'Tactical Summary' for the top 1% of Hispanic tech leaders. Focus on the cost-for-performance ratio.
        
        LENGTH: 300-400 words. Keep it punchy and spaced out.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a world-class strategic advisor. You make complex tech look like a simple business decision. You hate bricks of text and love clarity."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=850 
            )
            content = response.choices[0].message.content
            if len(content) > 2900:
                content = content[:2897] + "..."
            return content
        except Exception as e:
            return f"Error with OpenAI: {e}"

    def get_growth_hacks(self, article):
        """
        Phase 18: Precise Identification.
        """
        author_name = article.get('author', 'the authors')
        clean_tag = author_name.replace(' ', '')
        
        hacks = f"""
        🚀 **ESTRATEGIA DE AUTORIDAD (VERSIÓN CIRUJANO):**
        
        **1. Identificando al Autor:**
        El Peter Chen correcto es **Peter L. Chen** o **Peter Lau-Luk Chen**. 
        - Es Researcher en **Columbia University**.
        - Su foto en LinkedIn suele ser profesional o académica.
        - En su perfil DEBE decir **Columbia University** y **AI/Reinforcement Learning**.
        
        **2. Comentario de Poder:**
        Publica este comentario para forzar la respuesta:
        "Excellent technical work on RACO, @{author_name.replace(' ', '')}. This multi-objective alignment approach solves the gradient conflict mess most teams are ignoring. How are you handling the entropy trade-offs in larger scales? 
        
        PD: Comment 'MAPA' for my technical integration guide. 👇"
        """
        return hacks

    def generate_carousel_slides(self, article, language='es'):
        """
        Crea 3 descripciones de imagen relevantes al contenido.
        """
        prompt = f"""
        Actúa como un Diseñador de Conceptos Técnicos. Contenido: {article['title']}
        TAREA: Crea 3 descripciones de imagen para DALL-E 3 que ilustren este contenido de forma realista.
        IDIOMA: INGLÉS.
        FORMATO: 3 líneas de texto separadas.
        """
        try:
            client = OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Solo devuelve 3 líneas de texto."},
                    {"role": "user", "content": prompt}
                ]
            )
            slides = [s.strip() for s in response.choices[0].message.content.split('\n') if len(s.strip()) > 10]
            while len(slides) < 3:
                slides.append(f"Candid photo of a professional analyzing {article['title']}, industrial lab style.")
            return slides[:3]
        except:
            return ["Raw photography of industrial technology"] * 3

    def create_pdf_from_images(self, image_paths, output_path="carousel.pdf"):
        import img2pdf
        try:
            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(image_paths))
            return output_path
        except Exception as e:
            print(f"Error creando PDF: {e}")
            return None

if __name__ == "__main__":
    bot = AIConsentBot()
    papers = bot.fetch_arxiv_papers(max_results=1)
    if papers:
        p = papers[0]
        print(f"Muestra: {p['title']}")
        print(bot.generate_linkedin_post(p))
