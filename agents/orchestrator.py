from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.search_agent import run_search_agent
from agents.summarizer_agent import run_summarizer_agent
from agents.report_agent import run_report_agent

# Define the shared state between agents
class ResearchState(TypedDict):
    query: str
    search_data: dict
    summary: str
    report: str

# Each node is one agent
def search_node(state: ResearchState) -> ResearchState:
    state["search_data"] = run_search_agent(state["query"])
    return state

def summarizer_node(state: ResearchState) -> ResearchState:
    state["summary"] = run_summarizer_agent(state["search_data"])
    return state

def report_node(state: ResearchState) -> ResearchState:
    state["report"] = run_report_agent(
        state["query"],
        state["summary"],
        state["search_data"]["results"]
    )
    return state

# Build the graph
def build_research_graph():
    graph = StateGraph(ResearchState)
    
    graph.add_node("search", search_node)
    graph.add_node("summarizer", summarizer_node)
    graph.add_node("report", report_node)
    
    graph.set_entry_point("search")
    graph.add_edge("search", "summarizer")
    graph.add_edge("summarizer", "report")
    graph.add_edge("report", END)
    
    return graph.compile()

def run_research_pipeline(query: str) -> str:
    """Run the full multi-agent research pipeline."""
    graph = build_research_graph()
    
    final_state = graph.invoke({
        "query": query,
        "search_data": {},
        "summary": "",
        "report": ""
    })
    
    return final_state["report"]