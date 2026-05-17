import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_summarizer_agent(search_data: dict) -> str:
    """Summarize raw search results into clean insights."""
    print("📝 Summarizing results...")
    
    # Prepare context from search results
    context = "\n\n".join([
        f"Source: {r['title']}\n{r['content']}"
        for r in search_data["results"][:6]
    ])
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""You are a research summarizer. Given these web search results about "{search_data['query']}", 
extract the key insights and facts. Be concise and factual.

SEARCH RESULTS:
{context}

Provide 5-7 key insights in bullet points."""
        }]
    )
    
    return message.content[0].text