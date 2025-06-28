from .base_optimizer import BasePromptOptimizer
from typing import Dict, Any

class TabnineOptimizer(BasePromptOptimizer):
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        analysis = {
            'intent': 'pattern_completion' if 'pattern' in prompt else 'function_extension' if 'extend' in prompt else 'class_implementation',
            'complexity': 'high' if len(prompt.split()) > 30 else 'low',
            'requirements': []
        }
        if 'team' in prompt:
            analysis['requirements'].append('team_convention')
        return analysis

    def optimize_prompt(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        strategies = self.tool_config.get('optimization_strategies', [])
        template = self.tool_config['prompt_templates'].get(analysis['intent'], None)
        explanation = []
        optimized_prompt = prompt
        if template:
            optimized_prompt = template.format(
                language='Python',
                pattern_name='singleton',
                code_snippet=prompt,
                additional_feature=prompt,
                existing_function=prompt,
                class_name='MyClass',
                architecture_pattern='MVC'
            )
            explanation.append(f"Used template for {analysis['intent']}.")
        explanation.extend([f"Applied: {s}" for s in strategies])
        return {
            'optimized_prompt': optimized_prompt,
            'explanation': '\n'.join(explanation)
        } 