import json
import os
from typing import List, Dict, Any

class AgentDatabase:
    def __init__(self, json_path: str = None):
        if json_path is None:
            json_path = os.path.join(os.path.dirname(__file__), 'agents_db.json')
        self.json_path = json_path
        self.agents = self._load_agents()
    
    def _load_agents(self) -> List[Dict[str, Any]]:
        """Load agent information from the database"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get all agents in the database"""
        return self.agents
    
    def get_agent_by_name(self, name: str) -> Dict[str, Any]:
        """Get a specific agent by name"""
        for agent in self.agents:
            if agent['name'].lower() == name.lower():
                return agent
        return None
    
    def search_agents(self, query: str) -> List[Dict[str, Any]]:
        """Search agents by name, description, or capabilities"""
        query = query.lower()
        results = []
        
        for agent in self.agents:
            if (query in agent['name'].lower() or 
                query in agent['description'].lower() or
                any(query in capability.lower() for capability in agent.get('capabilities', [])) or
                any(query in strength.lower() for strength in agent.get('strengths', []))):
                results.append(agent)
        
        return results 