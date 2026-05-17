from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, max_results: int = 5) -> dict:
    """Search the web using Tavily and return clean results."""
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=True
    )
    
    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", "")
        })
    
    return {
        "answer": response.get("answer", ""),
        "results": results
    }