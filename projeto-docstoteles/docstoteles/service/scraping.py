import os
from firecrawl import FirecrawlApp

class ScrapingService:
    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        self.api_url = os.getenv("FIRECRAWL_API_URL")
        self.app = FirecrawlApp(api_key=self.api_key, api_url=self.api_url)
    
    def scrape_website(self, url, collection_name):
        """Executa o mapeamento e o scraping de um site"""
        try:
            # 1. Mapear o site para encontrar URLs relevantes
            map_result = self.app.map_url(url)
            
            # Extrair links (suporta diferentes versões do SDK)
            links = []
            if isinstance(map_result, dict):
                links = map_result.get("links", []) or map_result.get("data", {}).get("links", [])
            else:
                links = getattr(map_result, 'links', []) or getattr(getattr(map_result, 'data', {}), 'links', [])
            
            # Limitar a 10 páginas para evitar estourar limites/tempo no protótipo
            links = links[:10]
            
            if not links:
                return {"success": False, "error": "Nenhum link encontrado no site informado."}
            
            # 2. Executar o batch scraping das URLs encontradas
            scrape_result = self.app.batch_scrape_urls(links)
            
            # Extrair os dados processados
            scraped_data = []
            if isinstance(scrape_result, dict):
                scraped_data = scrape_result.get("data", [])
            else:
                scraped_data = getattr(scrape_result, 'data', [])
            
            # 3. Salvar o conteúdo em arquivos Markdown locais
            collection_path = f"data/collections/{collection_name}"
            os.makedirs(collection_path, exist_ok=True)
            
            saved_count = 0
            for i, page in enumerate(scraped_data, 1):
                # Tentar extrair o markdown de várias formas possíveis (SDK robusto)
                markdown_content = ""
                if isinstance(page, dict):
                    markdown_content = page.get("markdown") or page.get("data", {}).get("markdown")
                else:
                    markdown_content = getattr(page, 'markdown', "") or getattr(getattr(page, 'data', {}), 'markdown', "")
                
                if markdown_content:
                    file_path = os.path.join(collection_path, f"doc_{i}.md")
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(markdown_content)
                    saved_count += 1
            
            return {"success": True, "files": saved_count}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
 