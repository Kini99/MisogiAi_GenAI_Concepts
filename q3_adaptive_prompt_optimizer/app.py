import os
import json
from flask import Flask, render_template, request
from optimizers.github_copilot_optimizer import GitHubCopilotOptimizer
from optimizers.cursor_optimizer import CursorOptimizer
from optimizers.replit_optimizer import ReplitOptimizer
from optimizers.amazon_codewhisperer_optimizer import AmazonCodeWhispererOptimizer
from optimizers.tabnine_optimizer import TabnineOptimizer
from optimizers.kite_optimizer import KiteOptimizer

app = Flask(__name__)

# Load tool analysis config
with open(os.path.join(os.path.dirname(__file__), 'tool_analysis.json'), 'r') as f:
    TOOL_CONFIG = json.load(f)['tools']

TOOL_OPTIMIZERS = {
    'github_copilot': GitHubCopilotOptimizer,
    'cursor': CursorOptimizer,
    'replit': ReplitOptimizer,
    'amazon_codewhisperer': AmazonCodeWhispererOptimizer,
    'tabnine': TabnineOptimizer,
    'kite': KiteOptimizer
}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        base_prompt = request.form['base_prompt']
        tool = request.form['tool']
        optimizer_cls = TOOL_OPTIMIZERS[tool]
        optimizer = optimizer_cls(TOOL_CONFIG[tool])
        analysis = optimizer.analyze_prompt(base_prompt)
        optimized = optimizer.optimize_prompt(base_prompt, analysis)
        result = {
            'base_prompt': base_prompt,
            'optimized_prompt': optimized['optimized_prompt'],
            'explanation': optimized['explanation'],
            'tool': TOOL_CONFIG[tool]['name']
        }
    return render_template('index.html', tools=TOOL_CONFIG, result=result)

if __name__ == '__main__':
    app.run(debug=True) 