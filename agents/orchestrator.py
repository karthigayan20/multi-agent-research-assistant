"""
Research Orchestrator
Manages the 3-agent pipeline:
    SearchAgent → AnalystAgent → ReportWriterAgent

Handles inter-agent communication, status callbacks, and error recovery.
"""

from typing import Any, Callable, Dict, Optional

from agents.search_agent import SearchAgent
from agents.analyst_agent import AnalystAgent
from agents.report_writer_agent import ReportWriterAgent


class ResearchOrchestrator:
    """
    Coordinates the 3-agent research pipeline.

    Pipeline:
        1. SearchAgent   — Web search via Tavily
        2. AnalystAgent  — Insight extraction and synthesis
        3. ReportWriter  — Final report compilation

    Each agent's output feeds directly into the next agent's input.
    A status_callback can be supplied to push live UI updates.
    """

    def __init__(
        self,
        groq_api_key: str,
        tavily_api_key: str,
        max_search_results: int = 5,
        status_callback: Optional[Callable[[str, str, bool], None]] = None,
    ):
        self.status_callback = status_callback or (lambda *_: None)

        # Instantiate agents
        self.search_agent = SearchAgent(
            groq_api_key=groq_api_key,
            tavily_api_key=tavily_api_key,
            max_results=max_search_results,
        )
        self.analyst_agent = AnalystAgent(groq_api_key=groq_api_key)
        self.report_writer = ReportWriterAgent(groq_api_key=groq_api_key)

    def run(self, topic: str) -> Dict[str, Any]:
        """
        Execute the full research pipeline for a given topic.

        Args:
            topic: The research subject

        Returns:
            Final report dict from ReportWriterAgent
        """
        # ── Step 1: Search ────────────────────────────────────────────────────
        self.status_callback(
            "search", f"Generating queries and searching the web for: '{topic}'", False
        )
        search_output = self.search_agent.run({"topic": topic})
        self.status_callback(
            "search",
            f"Found {search_output['sources_count']} relevant sources.",
            True,
        )

        # ── Step 2: Analysis ──────────────────────────────────────────────────
        self.status_callback(
            "analyst", "Reading search results and extracting key insights...", False
        )
        analyst_output = self.analyst_agent.run(search_output)
        self.status_callback(
            "analyst",
            f"Extracted {len(analyst_output['insights'])} insights across "
            f"{len(analyst_output['themes'])} themes.",
            True,
        )

        # ── Step 3: Report Writing ─────────────────────────────────────────────
        self.status_callback(
            "writer", "Compiling structured research report...", False
        )
        report_output = self.report_writer.run(analyst_output)
        self.status_callback("writer", "Report complete and ready.", True)

        return report_output
