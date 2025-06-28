from flask import Flask, render_template, request, jsonify
import os
from recommendation_engine import RecommendationEngine

app = Flask(__name__)

# Check for required environment variable
if not os.getenv('GOOGLE_API_KEY'):
    print("Warning: GOOGLE_API_KEY environment variable not set. Please set it to use Gemini 2.0 Flash.")
    recommendation_engine = None
else:
    try:
        recommendation_engine = RecommendationEngine()
    except Exception as e:
        print(f"Error initializing recommendation engine: {e}")
        recommendation_engine = None

@app.route('/')
def index():
    """Main page with task input interface"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """API endpoint for getting agent recommendations"""
    if not recommendation_engine:
        return jsonify({
            'error': 'Recommendation engine not available. Please set GOOGLE_API_KEY environment variable.'
        }), 500
    
    try:
        data = request.get_json()
        task_description = data.get('task_description', '')
        
        if not task_description.strip():
            return jsonify({'error': 'Task description is required'}), 400
        
        # Get recommendations from the engine
        recommendations = recommendation_engine.get_recommendations(task_description)
        task_analysis = recommendation_engine.analyze_task(task_description)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'task_analysis': task_analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/agents')
def agents():
    """Page showing all available agents and their capabilities"""
    if not recommendation_engine:
        return jsonify({
            'error': 'Recommendation engine not available. Please set GOOGLE_API_KEY environment variable.'
        }), 500
    
    agents_info = recommendation_engine.get_all_agents()
    return render_template('agents.html', agents=agents_info)

@app.route('/api/agents')
def api_agents():
    """API endpoint for getting all agents information"""
    if not recommendation_engine:
        return jsonify({
            'error': 'Recommendation engine not available. Please set GOOGLE_API_KEY environment variable.'
        }), 500
    
    agents_info = recommendation_engine.get_all_agents()
    return jsonify(agents_info)

@app.route('/api/gemini_prompt', methods=['POST'])
def api_gemini_prompt():
    """API endpoint for generating Gemini prompt (for debugging)"""
    if not recommendation_engine:
        return jsonify({
            'error': 'Recommendation engine not available. Please set GOOGLE_API_KEY environment variable.'
        }), 500
    
    data = request.get_json()
    task_description = data.get('task_description', '')
    if not task_description.strip():
        return jsonify({'error': 'Task description is required'}), 400
    
    prompt = recommendation_engine.generate_gemini_prompt(task_description)
    return jsonify({'prompt': prompt})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gemini_available': recommendation_engine is not None,
        'api_key_set': bool(os.getenv('GOOGLE_API_KEY'))
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 