import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import run_research_pipeline

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 AI Research Assistant")
st.markdown("*Multi-agent research system powered by Claude + Tavily*")

st.divider()

query = st.text_input(
    "What do you want to research?",
    placeholder="e.g. future of quantum computing, best practices for MLOps..."
)

if st.button("🚀 Run Research", type="primary"):
    if not query.strip():
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("🔍 Searching the web..."):
            from agents.search_agent import run_search_agent
            search_data = run_search_agent(query)

        with st.spinner("📝 Summarizing findings..."):
            from agents.summarizer_agent import run_summarizer_agent
            summary = run_summarizer_agent(search_data)

        with st.spinner("📄 Generating report..."):
            from agents.report_agent import run_report_agent
            report = run_report_agent(query, summary, search_data["results"])

        st.success("✅ Research complete!")
        st.divider()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(report)

        with col2:
            st.subheader("📚 Sources")
            for r in search_data["results"][:6]:
                st.markdown(f"[{r['title']}]({r['url']})")

            st.subheader("💡 Quick Summary")
            st.info(summary[:500] + "...")