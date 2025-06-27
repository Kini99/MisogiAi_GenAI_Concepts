from flask import Flask, render_template, request, jsonify
from inference_calculator import LLMInferenceCalculator
import json

app = Flask(__name__)
calculator = LLMInferenceCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # Extract parameters
        model_size = data.get('model_size', '7B')
        tokens = int(data.get('tokens', 1024))
        batch_size = int(data.get('batch_size', 1))
        hardware_type = data.get('hardware_type', 'RTX4090')
        deployment_mode = data.get('deployment_mode', 'local')
        requests_per_hour = int(data.get('requests_per_hour', 100))
        
        # Calculate metrics
        result = calculator.calculate_inference_metrics(
            model_size=model_size,
            tokens=tokens,
            batch_size=batch_size,
            hardware_type=hardware_type,
            deployment_mode=deployment_mode,
            requests_per_hour=requests_per_hour
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/models')
def get_models():
    models = list(calculator.model_specs.keys())
    return jsonify(models)

@app.route('/api/hardware')
def get_hardware():
    hardware = list(calculator.hardware_specs.keys())
    return jsonify(hardware)

@app.route('/api/deployment_modes')
def get_deployment_modes():
    modes = ['local', 'cloud', 'edge']
    return jsonify(modes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 