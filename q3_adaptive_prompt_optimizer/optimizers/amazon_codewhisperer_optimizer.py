from .base_optimizer import BasePromptOptimizer
from typing import Dict, Any

class AmazonCodeWhispererOptimizer(BasePromptOptimizer):
    def analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        analysis = {
            'intent': 'aws_integration' if 'AWS' in prompt or 'S3' in prompt else 'lambda_function' if 'Lambda' in prompt else 'cloudformation',
            'complexity': 'high' if len(prompt.split()) > 30 else 'low',
            'requirements': []
        }
        if 'security' in prompt:
            analysis['requirements'].append('security')
        return analysis

    def optimize_prompt(self, prompt: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        strategies = self.tool_config.get('optimization_strategies', [])
        template = self.tool_config['prompt_templates'].get(analysis['intent'], None)
        explanation = []
        optimized_prompt = prompt
        if template:
            optimized_prompt = template.format(
                language='Python',
                aws_service='S3',
                description=prompt,
                resource_type='S3 Bucket',
                requirements=prompt
            )
            explanation.append(f"Used template for {analysis['intent']}.")
        explanation.extend([f"Applied: {s}" for s in strategies])
        return {
            'optimized_prompt': optimized_prompt,
            'explanation': '\n'.join(explanation)
        } 