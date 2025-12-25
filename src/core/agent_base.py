from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class AgentContext:
    """Shared state passed between agents."""
    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        self._data = initial_data or {}

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def set(self, key: str, value: Any):
        self._data[key] = value

    def to_dict(self) -> Dict[str, Any]:
        return self._data

class Agent(ABC):
    """Base class for all agents."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(self, context: AgentContext) -> None:
        """
        Execute the agent's logic.
        Agents read from context and write back to context.
        """
        pass

    def __repr__(self):
        return f"<Agent: {self.name}>"
