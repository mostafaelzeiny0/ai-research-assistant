from tools.search import search_web

def run_search_agent(query: str) -> dict:
    """Search the web and return structured results."""
    print(f"🔍 Searching for: {query}")
    
    # Break query into 3 sub-queries for better coverage
    sub_queries = [
        query,
        f"{query} latest developments",
        f"{query} detailed analysis"
    ]
    
    all_results = []
    answers = []
    
    for q in sub_queries:
        data = search_web(q, max_results=3)
        all_results.extend(data["results"])
        if data["answer"]:
            answers.append(data["answer"])
    
    return {
        "query": query,
        "answers": answers,
        "results": all_results
    }