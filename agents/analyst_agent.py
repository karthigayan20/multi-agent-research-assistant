"""
Analyst Agent
Reads raw search results and extracts structured insights, themes, and key findings.
"""

import json
from typing import Any, Dict, List

from agents.base_agent import BaseAgent


ANALYST_SYSTEM_PROMPT = """You are a senior research analyst with expertise in synthesizing
information from multiple sources. Your job is to:
1. Read raw search results on a topic
2. Identify the most important facts, trends, and insights
3. Eliminate redundant information
4. Organize findings into clear, numbered insights
5. Note any conflicting information or knowledge gaps

Be objective, precise, and cite sources by their [Source N] label.
"""


class AnalystAgent(BaseAgent):
    """
    Agent 2 — Research Analyst
    Synthesizes raw search data into structured insights.
    """

    def __init__(self, groq_api_key: str):
        super().__init__(groq_api_key=groq_api_key, temperature=0.2, max_tokens=3000)

    @property
    def role(self) -> str:
        return "Senior Research Analyst"

    @property
    def goal(self) -> str:
        return (
            "Synthesize raw search results into structured, actionable insights "
            "that capture the most important information about the topic."
        )

    @property
    def backstory(self) -> str:
        return (
            "You are a seasoned analyst with 10 years of experience turning "
            "raw information into clear, structured intelligence reports. "
            "You are known for your ability to spot the signal in the noise."
        )

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Args:
            inputs: {
                "topic": str,
                "formatted_content": str,   from SearchAgent
                "raw_results": List[dict],
            }
        Returns:
            {
                "topic": str,
                "insights": List[str],
                "themes": List[str],
                "gaps": str,
                "raw_results": List[dict],  passed through for report writer
            }
        """
        topic = inputs["topic"]
        content = inputs["formatted_content"]

        # Extract insights
        insights_text = self._extract_insights(topic, content)
        insights = self._parse_numbered_list(insights_text)

        # Extract key themes
        themes = self._extract_themes(topic, insights_text)

        # Identify knowledge gaps
        gaps = self._identify_gaps(topic, insights_text)

        return {
            "topic": topic,
            "insights": insights,
            "insights_text": insights_text,
            "themes": themes,
            "gaps": gaps,
            "raw_results": inputs.get("raw_results", []),
            "sources_count": inputs.get("sources_count", 0),
        }

    # ── Private helpers ───────────────────────────────────────────────────────

    def _extract_insights(self, topic: str, content: str) -> str:
        user_prompt = f"""Topic: {topic}

Raw Search Results:
{content}

Extract 6-10 of the most important insights from these results.
Format as a numbered list. Each insight should be 1-3 sentences.
Cite the source number where applicable (e.g., "[Source 2]").
"""
        return self._call_llm(ANALYST_SYSTEM_PROMPT, user_prompt)

    def _extract_themes(self, topic: str, insights_text: str) -> List[str]:
        user_prompt = f"""Based on these insights about "{topic}":

{insights_text}

List 3-5 overarching themes or trends. Return ONLY a Python list of short
theme strings, one per line, no bullet points, no numbering."""
        result = self._call_llm(ANALYST_SYSTEM_PROMPT, user_prompt)
        themes = [t.strip().strip("-•*") for t in result.split("\n") if t.strip()]
        return themes[:5]

    def _identify_gaps(self, topic: str, insights_text: str) -> str:
        user_prompt = f"""Based on the research collected about "{topic}":

{insights_text}

In 2-3 sentences, describe what important aspects of this topic are missing
or not well-covered by the available sources. What would a researcher still
need to investigate?"""
        return self._call_llm(ANALYST_SYSTEM_PROMPT, user_prompt)

    @staticmethod
    def _parse_numbered_list(text: str) -> List[str]:
        """Parse a numbered list string into individual items."""
        lines = text.split("\n")
        items = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Remove leading numbers like "1.", "1)", etc.
            import re
            cleaned = re.sub(r"^\d+[.)]\s*", "", line)
            if cleaned:
                items.append(cleaned)
        return items
