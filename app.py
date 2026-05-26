"""
Multi-Agent Research Assistant - Main Application
Author: Built with LangChain + Groq + Tavily
"""

import streamlit as st
import os
from dotenv import load_dotenv

from agents.orchestrator import ResearchOrchestrator

load_dotenv()

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #0f172a; }
    .sub-header  { font-size: 1rem; color: #64748b; margin-bottom: 1.5rem; }
    .agent-card  {
        border-left: 4px solid;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        background: #f8fafc;
    }
    .agent-search    { border-color: #3b82f6; }
    .agent-analyst   { border-color: #8b5cf6; }
    .agent-writer    { border-color: #10b981; }
    .agent-label     { font-weight: 600; font-size: 0.85rem; }
    .report-section  { background: #f0fdf4; border-radius: 10px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────────────────────
if "research_history" not in st.session_state:
    st.session_state.research_history = []
if "current_report" not in st.session_state:
    st.session_state.current_report = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🔬 Multi-Agent Research Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Give it a topic — three specialized AI agents collaborate to '
    'search the web, analyze findings, and write a structured research report.</div>',
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ API Keys")

    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Free at console.groq.com",
        placeholder="gsk_...",
    )
    tavily_api_key = st.text_input(
        "Tavily API Key",
        type="password",
        value=os.getenv("TAVILY_API_KEY", ""),
        help="Free at app.tavily.com",
        placeholder="tvly-...",
    )

    st.markdown("---")
    st.header("🤖 Agent Pipeline")
    st.markdown("""
**Agent 1 — 🔍 Search Agent**
Searches the web for relevant, up-to-date information on your topic.

**Agent 2 — 🧠 Analyst Agent**
Synthesizes raw search results, extracts key insights, and identifies themes.

**Agent 3 — ✍️ Report Writer Agent**
Compiles a well-structured research report with sections, findings, and sources.
""")

    st.markdown("---")
    st.header("⚙️ Settings")
    report_depth = st.select_slider(
        "Research Depth",
        options=["Quick", "Standard", "Deep"],
        value="Standard",
    )
    depth_map = {"Quick": 3, "Standard": 5, "Deep": 8}
    max_results = depth_map[report_depth]

    st.markdown("---")
    st.markdown("**🔗 Tech Stack**")
    st.markdown("- 🧠 **LLM:** Groq (Llama 3)")
    st.markdown("- 🔍 **Search:** Tavily API")
    st.markdown("- 🤝 **Framework:** Custom multi-agent")
    st.markdown("- 🖥️ **UI:** Streamlit")

    if st.session_state.research_history:
        st.markdown("---")
        st.header("📋 History")
        for i, item in enumerate(reversed(st.session_state.research_history[-5:]), 1):
            st.caption(f"{i}. {item['topic'][:40]}...")

# ── Main Input Area ───────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])

with col_input:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Impact of LLMs on software engineering jobs in 2025",
        label_visibility="collapsed",
    )

with col_btn:
    run_btn = st.button("🚀 Research", type="primary", use_container_width=True)

# ── Run Research ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a research topic.")
    elif not groq_api_key:
        st.error("❌ Groq API key is required.")
    elif not tavily_api_key:
        st.error("❌ Tavily API key is required.")
    else:
        st.session_state.current_report = None

        # ── Live agent status display ─────────────────────────────────────────
        status_area = st.empty()

        with st.spinner(""):
            # Progress container
            progress_container = st.container()
            with progress_container:
                agent1_placeholder = st.empty()
                agent2_placeholder = st.empty()
                agent3_placeholder = st.empty()

            def update_status(agent: str, status: str, done: bool = False):
                icons = {
                    "search":  ("🔍", "agent-search",  "Search Agent"),
                    "analyst": ("🧠", "agent-analyst", "Analyst Agent"),
                    "writer":  ("✍️", "agent-writer",  "Report Writer"),
                }
                icon, cls, label = icons[agent]
                state_icon = "✅" if done else "⏳"
                html = (
                    f'<div class="agent-card {cls}">'
                    f'<span class="agent-label">{icon} {label}</span> {state_icon}<br>'
                    f'<small>{status}</small></div>'
                )
                if agent == "search":
                    agent1_placeholder.markdown(html, unsafe_allow_html=True)
                elif agent == "analyst":
                    agent2_placeholder.markdown(html, unsafe_allow_html=True)
                elif agent == "writer":
                    agent3_placeholder.markdown(html, unsafe_allow_html=True)

            try:
                orchestrator = ResearchOrchestrator(
                    groq_api_key=groq_api_key,
                    tavily_api_key=tavily_api_key,
                    max_search_results=max_results,
                    status_callback=update_status,
                )

                report = orchestrator.run(topic=topic)

                # Clear live status
                agent1_placeholder.empty()
                agent2_placeholder.empty()
                agent3_placeholder.empty()

                st.session_state.current_report = report
                st.session_state.research_history.append(
                    {"topic": topic, "report": report}
                )

            except Exception as e:
                agent1_placeholder.empty()
                agent2_placeholder.empty()
                agent3_placeholder.empty()
                st.error(f"❌ Research failed: {str(e)}")

# ── Report Display ────────────────────────────────────────────────────────────
if st.session_state.current_report:
    report = st.session_state.current_report
    st.markdown("---")

    col_title, col_dl = st.columns([4, 1])
    with col_title:
        st.subheader(f"📄 Research Report: {report.get('topic', topic)}")
    with col_dl:
        st.download_button(
            label="⬇️ Download .md",
            data=report.get("markdown", ""),
            file_name=f"research_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # ── Metadata bar ─────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sources Found", report.get("sources_count", 0))
    with col2:
        st.metric("Key Insights", report.get("insights_count", 0))
    with col3:
        st.metric("Report Depth", report_depth)

    st.markdown("---")

    # ── Tabs: Report | Raw Insights | Sources ─────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📄 Full Report", "🧠 Raw Insights", "🔗 Sources"])

    with tab1:
        st.markdown(report.get("final_report", "No report generated."))

    with tab2:
        st.markdown("### What the Analyst Agent found:")
        for i, insight in enumerate(report.get("insights", []), 1):
            with st.expander(f"Insight {i}: {insight[:80]}..."):
                st.write(insight)

    with tab3:
        st.markdown("### Sources used by Search Agent:")
        for i, source in enumerate(report.get("sources", []), 1):
            st.markdown(f"**{i}.** [{source.get('title', 'Untitled')}]({source.get('url', '#')})")
            st.caption(source.get("snippet", "")[:200] + "...")

else:
    if not run_btn:
        st.markdown("---")
        st.markdown("### 💡 Example Topics")
        examples = [
            "Advancements in multimodal AI models in 2025",
            "How RAG systems are changing enterprise search",
            "State of electric vehicle adoption in India",
            "Agentic AI frameworks — LangGraph vs CrewAI vs AutoGen",
            "Quantum computing breakthroughs in 2024-2025",
        ]
        cols = st.columns(len(examples))
        for col, ex in zip(cols, examples):
            with col:
                if st.button(ex, use_container_width=True):
                    st.session_state["prefill_topic"] = ex
                    st.rerun()
