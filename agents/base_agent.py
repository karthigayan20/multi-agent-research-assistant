"""
Base Agent
Abstract base class that all specialized agents inherit from.
Provides shared LLM access and a standard invoke interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage


class BaseAgent(ABC):
    """
    Every agent gets:
      - A Groq-backed LLM
      - A role, goal, and backstory (mirroring CrewAI design)
      - A standard `run(inputs) -> outputs` interface
    """

    def __init__(
        self,
        groq_api_key: str,
        model: str = "llama3-8b-8192",
        temperature: float = 0.2,
        max_tokens: int = 2048,
    ):
        self.llm = ChatGroq(
            api_key=groq_api_key,
            model_name=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    @property
    @abstractmethod
    def role(self) -> str:
        """Short role name (e.g. 'Search Agent')"""

    @property
    @abstractmethod
    def goal(self) -> str:
        """What this agent is trying to accomplish"""

    @property
    @abstractmethod
    def backstory(self) -> str:
        """Persona / expertise description for system prompt"""

    @abstractmethod
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task.

        Args:
            inputs: dict of required inputs for this agent
        Returns:
            dict of outputs to pass to the next agent
        """

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Helper to call the LLM with system + user messages."""
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        response = self.llm.invoke(messages)
        return response.content.strip()
