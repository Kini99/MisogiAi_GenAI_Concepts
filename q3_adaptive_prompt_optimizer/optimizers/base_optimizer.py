import abc
from typing import Dict, Any

class BasePromptOptimizer(abc.ABC):
    def __init__(self, tool_config: Dict[str, Any]):
        self.tool_config = tool_config

    @abc.abstractmethod
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the prompt for intent, complexity, and requirements."""
        pass

    @abc.abstractmethod
    def optimize_prompt(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Return a dict with keys: 'optimized_prompt', 'explanation'."""
        pass 