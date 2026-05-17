import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_report_agent(query: str, summary: str, sources: list) -> str:
    """Generate a final structured research report."""
    print("📄 Generating report...")
    
    sources_text = "\n".join([
        f"- {r['title']}: {r['url']}"
        for r in sources[:6]
    ])
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""You are a professional research analyst. Write a structured research report on:

TOPIC: {query}

KEY INSIGHTS:
{summary}

FORMAT YOUR REPORT AS:
# Research Report: {query}

## Executive Summary
(2-3 sentences)

## Key Findings
(detailed paragraphs)

## Conclusion
(actionable takeaways)

## Sources
{sources_text}"""
        }]
    )
    
    return message.content[0].text