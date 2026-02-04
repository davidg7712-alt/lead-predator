import arxiv
import datetime

def test_arxiv_search():
    print("🚀 Probando el Radar Científico (ArXiv)...")
    
    # Buscamos papers recientes en IA y Robótica
    search = arxiv.Search(
        query="cat:cs.AI OR cat:cs.RO",
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    for result in search.results():
        print(f"\n📄 Título: {result.title}")
        print(f"🔗 Link: {result.pdf_url}")
        print(f"🧠 Resumen (Abstract): {result.summary[:200]}...")
        print("-" * 30)

if __name__ == "__main__":
    test_arxiv_search()
