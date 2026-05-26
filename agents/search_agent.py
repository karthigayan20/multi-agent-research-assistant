"""
Search Agent
Uses the Tavily API to search the web and collect raw results for a given topic.
"""

from typing import Any, Dict, List

from tavily import TavilyClient

from agents.base_agent import BaseAgent


class SearchAgent(BaseAgent):
    """
    Agent 1 — Web Researcher
    Searches the internet and returns structured search results.
    """

    def __init__(self, groq_api_key: str, tavily_api_key: str, max_results: int = 5):
        super().__init__(groq_api_key=groq_api_key, temperature=0.0)
        self.tavily = TavilyClient(api_key=tavily_api_key)
        self.max_results = max_results

    @property
    def role(self) -> str:
        return "Web Research Specialist"

    @property
    def goal(self) -> str:
        return "Gather comprehensive, up-to-date information about a given topic from the web."

    @property
    def backstory(self) -> str:
        return (
            "You are an expert researcher with a talent for finding reliable, "
            "relevant information quickly. You know how to break a broad topic "
            "into focused search queries and evaluate source quality."
        )

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            inputs: {"topic": str}
        Returns:
            {
                "topic": str,
                "raw_results": List[dict],   # full Tavily hits
                "formatted_content": str,    # concatenated text for analyst
            }
        """
        topic = inputs["topic"]

        # Generate 2-3 targeted sub-queries using the LLM
        sub_queries = self._generate_queries(topic)

        all_results: List[dict] = []
        seen_urls = set()

        for query in sub_queries:
            try:
                response = self.tavily.search(
                    query=query,
                    search_depth="advanced",
                    max_results=self.max_results,
                    include_answer=True,
                )
                for r in response.get("results", []):
                    if r["url"] not in seen_urls:
                        all_results.append(
                            {
                                "title": r.get("title", "Untitled"),
                                "url": r.get("url", ""),
                                "snippet": r.get("content", ""),
                                "score": r.get("score", 0),
                            }
                        )
                        seen_urls.add(r["url"])
            except Exception as e:
                # Log and continue — don't let one bad query kill the pipeline
                print(f"[SearchAgent] Query failed: {query!r} — {e}")
                continue

        # Sort by relevance score
        all_results.sort(key=lambda x: x["score"], reverse=True)

        # Build a readable content block for the analyst
        formatted_parts = []
        for i, r in enumerate(all_results, 1):
            formatted_parts.append(
                f"[Source {i}] {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Content: {r['snippet']}\n"
            )
        formatted_content = "\n---\n".join(formatted_parts)

        return {
            "topic": topic,
            "raw_results": all_results,
            "formatted_content": formatted_content,
            "sources_count": len(all_results),
        }

    # ── Private helpers ───────────────────────────────────────────────────────

    def _generate_queries(self, topic: str) -> List[str]:
        """Ask the LLM to generate 3 targeted search queries for the topic."""
        system = (
            "You are a search query specialist. Given a research topic, "
            "generate exactly 3 focused search queries that together will cover "
            "the topic comprehensively. Return ONLY the 3 queries, one per line, "
            "no numbering, no extra text."
        )
        user = f"Topic: {topic}"
        result = self._call_llm(system, user)
        queries = [q.strip() for q in result.split("\n") if q.strip()]
        # Fallback to the raw topic if parsing fails
        return queries[:3] if queries else [topic]
