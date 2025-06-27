# LLM Inference Calculator

A comprehensive calculator for estimating LLM inference costs, latency, and memory usage across different models, hardware configurations, and deployment scenarios.

## Features

- **Multi-Model Support**: 7B, 13B, and GPT-4 parameter models
- **Hardware Analysis**: V100, A100, H100, RTX 4090, and CPU configurations
- **Deployment Modes**: Local, cloud, and edge deployment analysis
- **Cost Estimation**: Per-request, hourly, and monthly cost calculations
- **Performance Metrics**: Latency, throughput, and memory utilization
- **Hardware Compatibility**: Automatic compatibility checking and recommendations
- **Web Interface**: Modern, responsive web frontend for easy interaction

## Quick Start

### Prerequisites

- Python 3.8 or higher

### Installation

1. Clone or download the project files
2. Navigate to the project directory:
   ```bash
   cd q1_llm_inference_calculator
   ```

3. Install dependencies (for web interface):
   ```bash
   pip install -r requirements.txt
   ```

4. Run the web application:
   ```bash
   python app.py
   ```

5. Open your browser and go to: `http://localhost:5000`

### Command Line Usage

For command-line usage without the web interface:

```bash
python inference_calculator.py
```

## Web Interface

The calculator includes a modern web interface with the following features:

### Input Parameters
- **Model Size**: Choose from 7B, 13B, or GPT-4 models
- **Tokens**: Number of tokens to process (1-8192)
- **Batch Size**: Number of requests to process together (1-32)
- **Hardware Type**: Select from RTX 4090, V100, A100, H100, or CPU
- **Deployment Mode**: Local, cloud, or edge deployment
- **Requests per Hour**: Expected request volume

### Results Display
- **Memory Usage**: Total memory required and compatibility status
- **Latency**: Response time and tokens per second
- **Cost Analysis**: Per-request and monthly costs
- **Performance Score**: Overall performance rating (0-100)
- **Recommendations**: Optimization suggestions

### Interactive Features
- Real-time parameter suggestions based on model/hardware selection
- Visual compatibility indicators
- Responsive design for mobile and desktop
- Error handling and validation

## Usage Examples

### Basic Usage

```python
from inference_calculator import LLMInferenceCalculator

# Initialize calculator
calculator = LLMInferenceCalculator()

# Calculate metrics for a 7B model on RTX 4090
result = calculator.calculate_inference_metrics(
    model_size="7B",
    tokens=1024,
    batch_size=1,
    hardware_type="RTX4090",
    deployment_mode="local",
    requests_per_hour=100
)

print(f"Memory Usage: {result['memory']['total_memory_gb']:.2f} GB")
print(f"Latency: {result['latency']['total_latency_seconds']:.2f} seconds")
print(f"Cost per request: ${result['cost']['cost_per_request']:.6f}")
```

### Advanced Usage

```python
# Compare multiple configurations
configurations = [
    {"model_size": "7B", "hardware_type": "RTX4090", "deployment_mode": "local"},
    {"model_size": "13B", "hardware_type": "A100", "deployment_mode": "cloud"},
    {"model_size": "GPT-4", "hardware_type": "H100", "deployment_mode": "cloud"}
]

for config in configurations:
    result = calculator.calculate_inference_metrics(
        tokens=2048,
        batch_size=4,
        requests_per_hour=50,
        **config
    )
    
    print(f"\n{config['model_size']} on {config['hardware_type']}:")
    print(f"  Memory: {result['memory']['total_memory_gb']:.1f} GB")
    print(f"  Latency: {result['latency']['total_latency_seconds']:.2f}s")
    print(f"  Monthly Cost: ${result['cost']['monthly_cost']:.2f}")
```

## Input Parameters

### Model Size
- **7B**: ~7 billion parameters, ~14 GB model size
- **13B**: ~13 billion parameters, ~26 GB model size  
- **GPT-4**: ~175 billion parameters, ~350 GB model size

### Hardware Types
- **RTX 4090**: 24 GB VRAM, consumer GPU
- **V100**: 16 GB VRAM, datacenter GPU
- **A100**: 40 GB VRAM, high-performance GPU
- **H100**: 80 GB VRAM, latest generation GPU
- **CPU**: 64 GB RAM, general-purpose computing

### Deployment Modes
- **local**: On-premises deployment
- **cloud**: Cloud-based deployment
- **edge**: Edge device deployment

## Output Metrics

### Memory Analysis
- **Model Memory**: Base model weights
- **KV Cache Memory**: Attention layer cache
- **Activation Memory**: Intermediate computations
- **Total Memory**: Complete memory requirement
- **Memory Utilization**: Percentage of hardware memory used

### Latency Analysis
- **Compute Latency**: GPU computation time
- **Memory Latency**: Memory bandwidth constraints
- **Model Latency**: Model-specific processing time
- **Total Latency**: Complete inference time
- **Tokens per Second**: Throughput metric

### Cost Analysis
- **Cost per Request**: Individual request cost
- **Power Cost**: Electricity consumption
- **Total Cost per Request**: Complete cost
- **Cost per 1K Tokens**: Normalized cost metric
- **Monthly Cost**: Extended period cost

### Compatibility Analysis
- **Memory Compatibility**: Whether model fits in hardware
- **Latency Acceptability**: Meets performance requirements
- **Performance Score**: Overall performance rating (0-100)
- **Recommendations**: Optimization suggestions

## Example Results

### 7B Model on RTX 4090 (Local)
```json
{
  "inputs": {
    "model_size": "7B",
    "tokens": 1024,
    "batch_size": 1,
    "hardware_type": "RTX4090",
    "deployment_mode": "local",
    "requests_per_hour": 100
  },
  "memory": {
    "total_memory_gb": 16.8,
    "memory_fits": true,
    "memory_utilization_percent": 70.0
  },
  "latency": {
    "total_latency_seconds": 2.46,
    "tokens_per_second": 416.7
  },
  "cost": {
    "cost_per_request": 0.00034,
    "monthly_cost": 24.48
  },
  "compatibility": {
    "performance_score": 85.0,
    "recommendations": ["Good performance for local deployment"]
  }
}
```

## Use Cases

### 1. Chatbot Development
- **Recommended**: 7B model on RTX 4090
- **Rationale**: Low latency, cost-effective, sufficient quality
- **Expected Cost**: ~$25/month for 100 requests/hour

### 2. Content Generation
- **Recommended**: 7B model on A100
- **Rationale**: Good quality, reasonable latency, cloud scalability
- **Expected Cost**: ~$235/month for 100 requests/hour

### 3. Code Assistant
- **Recommended**: 7B model on RTX 4090
- **Rationale**: Fast response, local privacy, cost-effective
- **Expected Cost**: ~$288/month for 5000 requests/hour

## Performance Optimization Tips

### Memory Optimization
1. **Use Quantization**: FP16 instead of FP32 reduces memory by 50%
2. **Optimize Batch Size**: Balance memory usage with throughput
3. **Consider Model Parallelism**: Split large models across multiple GPUs
4. **Implement Offloading**: Move parts to CPU/RAM when possible

### Latency Optimization
1. **Choose Appropriate Hardware**: Match GPU to model requirements
2. **Optimize Batch Processing**: Process multiple requests together
3. **Use Caching**: Cache common responses and intermediate results
4. **Consider Model Compression**: Smaller models for faster inference

### Cost Optimization
1. **Right-Size Models**: Use smallest model that meets quality requirements
2. **Optimize Hardware Selection**: Balance performance and cost
3. **Implement Request Batching**: Reduce per-request overhead
4. **Monitor Usage Patterns**: Scale resources based on demand

## Hardware Recommendations

### For Local Development
- **RTX 4090**: Best price/performance for 7B models
- **A100**: Good for 13B models if budget allows
- **CPU**: Fallback option for small models

### For Production Deployment
- **A100**: Optimal for most production workloads
- **H100**: For high-performance requirements
- **Multiple GPUs**: For large models or high throughput

### For Edge Deployment
- **RTX 4090**: Best consumer GPU option
- **CPU**: For resource-constrained environments
- **Specialized Hardware**: Consider dedicated inference accelerators

## Limitations

1. **Estimates Only**: Results are approximations based on theoretical models
2. **Hardware Variations**: Actual performance may vary by specific hardware
3. **Model Differences**: Different model architectures may have different characteristics
4. **Network Overhead**: Cloud deployment includes additional network latency
5. **Software Stack**: Performance depends on inference framework and optimizations

## References

- [LLM Inference Calculator](https://llm-inference-calculator-rki02.kinsta.page/)
- [VRAM Calculator](https://apxml.com/tools/vram-calculator)
- Research notes and scenario analysis included in project files

