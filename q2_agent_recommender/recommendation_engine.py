import json
import os
import google.generativeai as genai
from typing import List, Dict, Any
from agent_database import AgentDatabase

class RecommendationEngine:
    def __init__(self):
        self.agent_db = AgentDatabase()
        # Initialize Gemini 2.0 Flash
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """Analyze the given task using Gemini 2.0 Flash"""
        prompt = f"""
        Analyze the following coding task and extract key characteristics:
        
        Task: {task_description}
        
        Please analyze and return a JSON object with the following structure:
        {{
            "task_type": "web_development|data_science|mobile_development|scripting|system_design|general",
            "complexity": "low|medium|high",
            "languages": ["list", "of", "programming", "languages"],
            "frameworks": ["list", "of", "frameworks", "or", "libraries"],
            "estimated_duration": "short|medium|long",
            "team_size": "individual|small_team|team",
            "key_requirements": ["list", "of", "key", "requirements"],
            "domain": "web|mobile|data|ai|backend|frontend|fullstack|other"
        }}
        
        Only return the JSON object, no additional text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            analysis = json.loads(response_text.strip())
            return analysis
        except Exception as e:
            # Fallback analysis
            return {
                "task_type": "general",
                "complexity": "medium",
                "languages": [],
                "frameworks": [],
                "estimated_duration": "medium",
                "team_size": "individual",
                "key_requirements": [],
                "domain": "other"
            }
    
    def get_recommendations(self, task_description: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Get top-k agent recommendations using Gemini 2.0 Flash"""
        # Analyze the task
        task_analysis = self.analyze_task(task_description)
        
        # Get all agents
        all_agents = self.agent_db.get_all_agents()
        
        # Create prompt for Gemini to recommend agents
        agents_json = json.dumps(all_agents, indent=2)
        
        prompt = f"""
        You are an expert AI coding agent recommender. You have access to a knowledge base of coding agents and a task analysis.

        Task Analysis:
        {json.dumps(task_analysis, indent=2)}

        Available Agents:
        {agents_json}

        Based on the task analysis and available agents, recommend the top {top_k} most suitable coding agents for this task.

        For each recommendation, provide:
        1. A score from 0.0 to 1.0 (higher is better)
        2. A detailed justification explaining why this agent is a good fit
        3. The complete agent information

        Return the result in this exact JSON format:
        {{
            "recommendations": [
                {{
                    "rank": 1,
                    "agent_name": "Agent Name",
                    "score": 0.85,
                    "justification": "Detailed explanation of why this agent is suitable...",
                    "agent_info": {{ ... complete agent object ... }}
                }},
                ...
            ]
        }}

        Only return the JSON object, no additional text.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            return result.get('recommendations', [])
        except Exception as e:
            # Fallback to basic recommendations
            return self._get_fallback_recommendations(task_analysis, all_agents, top_k)
    
    def _get_fallback_recommendations(self, task_analysis: Dict[str, Any], all_agents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
        """Fallback recommendation method if Gemini fails"""
        recommendations = []
        
        # Simple scoring based on task type and capabilities
        scored_agents = []
        for agent in all_agents:
            score = 0.0
            
            # Task type matching
            task_type = task_analysis.get('task_type', 'general')
            if task_type in agent.get('strengths', []):
                score += 0.4
            elif task_type in agent.get('capabilities', []):
                score += 0.2
            
            # Language matching
            languages = task_analysis.get('languages', [])
            agent_languages = agent.get('languages', [])
            if languages and agent_languages:
                language_overlap = len(set(languages) & set(agent_languages))
                if language_overlap > 0:
                    score += 0.3 * (language_overlap / len(languages))
            
            # Framework matching
            frameworks = task_analysis.get('frameworks', [])
            agent_frameworks = agent.get('frameworks', [])
            if frameworks and agent_frameworks:
                framework_overlap = len(set(frameworks) & set(agent_frameworks))
                if framework_overlap > 0:
                    score += 0.3 * (framework_overlap / len(frameworks))
            
            scored_agents.append({
                'agent': agent,
                'score': score
            })
        
        # Sort by score and return top-k
        scored_agents.sort(key=lambda x: x['score'], reverse=True)
        
        for i, scored_agent in enumerate(scored_agents[:top_k]):
            recommendation = {
                'rank': i + 1,
                'agent_name': scored_agent['agent']['name'],
                'score': round(scored_agent['score'], 2),
                'justification': f"Recommended based on task type '{task_analysis.get('task_type', 'general')}' and language/framework compatibility.",
                'agent_info': scored_agent['agent']
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Get information about all available agents"""
        return self.agent_db.get_all_agents()

    def generate_gemini_prompt(self, task_description: str) -> str:
        """
        Generate a prompt for Gemini 2.0 Flash to analyze the task and recommend agents.
        """
        with open(self.agent_db.json_path, 'r', encoding='utf-8') as f:
            agents_json = f.read()
        
        prompt = f'''
You are an expert AI coding agent recommender.

You have access to a knowledge base of coding agents in JSON format (see below). Each agent has fields like name, description, company, model, strengths, capabilities, languages, frameworks, complexity_handling, system_prompt, pricing, website, and integration.

Given a user's natural language coding task description, do the following:
1. Analyze the task and extract:
   - task_type (e.g., web_development, data_science, scripting, etc.)
   - complexity (low, medium, high)
   - languages (list)
   - frameworks (list)
   - estimated_duration (short, medium, long)
   - team_size (individual, small_team, team)
   - key_requirements (list)
   - domain (web, mobile, data, ai, backend, frontend, fullstack, other)
2. Using the knowledge base, recommend the top 3 most suitable coding agents for the task.
   - For each agent, provide:
     - agent_name
     - score (0.0 to 1.0, higher is better)
     - justification (why this agent is a good fit)
     - agent_info (all fields from the knowledge base for that agent)
3. Return the result in the following JSON format:

{{
  "task_analysis": {{
    "task_type": "...",
    "complexity": "...",
    "languages": [...],
    "frameworks": [...],
    "estimated_duration": "...",
    "team_size": "...",
    "key_requirements": [...],
    "domain": "..."
  }},
  "recommendations": [
    {{
      "rank": 1,
      "agent_name": "...",
      "score": 0.85,
      "justification": "...",
      "agent_info": {{ ... }}
    }},
    ...
  ]
}}

Here is the agent knowledge base:
{agents_json}

User's task description:
{task_description}
'''
        return prompt 