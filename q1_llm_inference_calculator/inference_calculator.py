import math
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ModelSize(Enum):
    """Supported model sizes"""
    SEVEN_B = "7B"
    THIRTEEN_B = "13B"
    GPT4 = "GPT-4"


class HardwareType(Enum):
    """Supported hardware types"""
    GPU_V100 = "V100"
    GPU_A100 = "A100"
    GPU_H100 = "H100"
    GPU_RTX4090 = "RTX4090"
    CPU = "CPU"


class DeploymentMode(Enum):
    """Deployment modes"""
    LOCAL = "local"
    CLOUD = "cloud"
    EDGE = "edge"


@dataclass
class HardwareSpecs:
    """Hardware specifications"""
    name: str
    vram_gb: float
    memory_bandwidth_gbps: float
    compute_tflops: float
    cost_per_hour: float
    power_consumption_w: float


@dataclass
class ModelSpecs:
    """Model specifications"""
    name: str
    parameters_billions: float
    model_size_gb: float
    context_window: int
    tokens_per_second: float
    memory_efficiency: float


class LLMInferenceCalculator:
    """Main calculator class for LLM inference estimates"""
    
    def __init__(self):
        self.hardware_specs = self._initialize_hardware_specs()
        self.model_specs = self._initialize_model_specs()
        
    def _initialize_hardware_specs(self) -> Dict[str, HardwareSpecs]:
        """Initialize hardware specifications"""
        return {
            HardwareType.GPU_V100.value: HardwareSpecs(
                name="NVIDIA V100",
                vram_gb=16.0,
                memory_bandwidth_gbps=900.0,
                compute_tflops=112.0,
                cost_per_hour=2.48,
                power_consumption_w=250.0
            ),
            HardwareType.GPU_A100.value: HardwareSpecs(
                name="NVIDIA A100",
                vram_gb=40.0,
                memory_bandwidth_gbps=1555.0,
                compute_tflops=312.0,
                cost_per_hour=3.26,
                power_consumption_w=400.0
            ),
            HardwareType.GPU_H100.value: HardwareSpecs(
                name="NVIDIA H100",
                vram_gb=80.0,
                memory_bandwidth_gbps=3350.0,
                compute_tflops=989.0,
                cost_per_hour=4.00,
                power_consumption_w=700.0
            ),
            HardwareType.GPU_RTX4090.value: HardwareSpecs(
                name="NVIDIA RTX 4090",
                vram_gb=24.0,
                memory_bandwidth_gbps=1008.0,
                compute_tflops=83.0,
                cost_per_hour=0.50,
                power_consumption_w=450.0
            ),
            HardwareType.CPU.value: HardwareSpecs(
                name="High-end CPU",
                vram_gb=64.0,
                memory_bandwidth_gbps=50.0,
                compute_tflops=1.0,
                cost_per_hour=0.10,
                power_consumption_w=150.0
            )
        }
    
    def _initialize_model_specs(self) -> Dict[str, ModelSpecs]:
        """Initialize model specifications"""
        return {
            ModelSize.SEVEN_B.value: ModelSpecs(
                name="7B Parameter Model",
                parameters_billions=7.0,
                model_size_gb=14.0,
                context_window=8192,
                tokens_per_second=50.0,
                memory_efficiency=0.85
            ),
            ModelSize.THIRTEEN_B.value: ModelSpecs(
                name="13B Parameter Model",
                parameters_billions=13.0,
                model_size_gb=26.0,
                context_window=8192,
                tokens_per_second=30.0,
                memory_efficiency=0.80
            ),
            ModelSize.GPT4.value: ModelSpecs(
                name="GPT-4",
                parameters_billions=175.0,
                model_size_gb=350.0,
                context_window=8192,
                tokens_per_second=15.0,
                memory_efficiency=0.90
            )
        }
    
    def calculate_memory_usage(self, model_size: str, tokens: int, batch_size: int, 
        hardware_type: str, deployment_mode: str) -> Dict[str, float]:
        """Calculate memory usage for inference"""
        model = self.model_specs[model_size]
        hardware = self.hardware_specs[hardware_type]
        
        # Base model memory (weights)
        model_memory_gb = model.model_size_gb
        
        # KV cache memory (depends on sequence length and batch size)
        kv_cache_memory_gb = (tokens * batch_size * model.parameters_billions * 2 * 4) / (1024**3)
        
        # Activation memory (rough estimate)
        activation_memory_gb = (tokens * batch_size * model.parameters_billions * 0.1) / (1024**3)
        
        # Total memory usage
        total_memory_gb = model_memory_gb + kv_cache_memory_gb + activation_memory_gb
        
        # Apply memory efficiency factor
        effective_memory_gb = total_memory_gb / model.memory_efficiency
        
        # Check if memory fits in hardware
        memory_fits = effective_memory_gb <= hardware.vram_gb
        
        return {
            "model_memory_gb": model_memory_gb,
            "kv_cache_memory_gb": kv_cache_memory_gb,
            "activation_memory_gb": activation_memory_gb,
            "total_memory_gb": total_memory_gb,
            "effective_memory_gb": effective_memory_gb,
            "hardware_memory_gb": hardware.vram_gb,
            "memory_fits": memory_fits,
            "memory_utilization_percent": (effective_memory_gb / hardware.vram_gb) * 100
        }
    
    def calculate_latency(self, model_size: str, tokens: int, batch_size: int,
        hardware_type: str, deployment_mode: str) -> Dict[str, float]:
        """Calculate inference latency"""
        model = self.model_specs[model_size]
        hardware = self.hardware_specs[hardware_type]
        
        # Base latency calculation based on model size and hardware
        # Simplified approach focusing on realistic estimates
        
        # Model-specific base latency (ms per token)
        base_latency_per_token_ms = {
            "7B": 20.0,    # ~50 tokens/second
            "13B": 33.0,   # ~30 tokens/second  
            "GPT-4": 67.0  # ~15 tokens/second
        }
        
        # Hardware efficiency factors
        hardware_efficiency = {
            "RTX4090": 1.0,
            "V100": 0.8,
            "A100": 0.6,
            "H100": 0.4,
            "CPU": 5.0
        }
        
        # Calculate base latency
        base_latency_ms = tokens * base_latency_per_token_ms[model_size]
        
        # Apply hardware efficiency
        hardware_adjusted_latency_ms = base_latency_ms * hardware_efficiency[hardware_type]
        
        # Apply deployment mode factors
        deployment_factors = {
            DeploymentMode.LOCAL.value: 1.0,
            DeploymentMode.CLOUD.value: 1.1,  # Slight network overhead
            DeploymentMode.EDGE.value: 1.3    # Limited resources
        }
        
        total_latency_ms = hardware_adjusted_latency_ms * deployment_factors[deployment_mode]
        
        # Calculate tokens per second
        tokens_per_second = tokens / (total_latency_ms / 1000)
        
        return {
            "compute_latency_ms": hardware_adjusted_latency_ms * 0.7,
            "memory_latency_ms": hardware_adjusted_latency_ms * 0.2,
            "model_latency_ms": hardware_adjusted_latency_ms * 0.1,
            "total_latency_ms": total_latency_ms,
            "total_latency_seconds": total_latency_ms / 1000,
            "tokens_per_second": tokens_per_second
        }
    
    def calculate_cost(self, model_size: str, tokens: int, batch_size: int,
        hardware_type: str, deployment_mode: str, requests_per_hour: int = 1) -> Dict[str, float]:
        """Calculate inference costs"""
        hardware = self.hardware_specs[hardware_type]
        
        # Calculate time per request
        latency_info = self.calculate_latency(model_size, tokens, batch_size, hardware_type, deployment_mode)
        time_per_request_hours = latency_info["total_latency_seconds"] / 3600
        
        # Cost per request
        cost_per_request = time_per_request_hours * hardware.cost_per_hour
        
        # Power cost (assuming $0.12/kWh)
        power_cost_per_hour = (hardware.power_consumption_w / 1000) * 0.12
        power_cost_per_request = time_per_request_hours * power_cost_per_hour
        
        # Total cost per request
        total_cost_per_request = cost_per_request + power_cost_per_request
        
        # Cost per 1K tokens
        cost_per_1k_tokens = (total_cost_per_request / tokens) * 1000
        
        # Hourly cost for given request rate
        hourly_cost = total_cost_per_request * requests_per_hour
        
        return {
            "cost_per_request": cost_per_request,
            "power_cost_per_request": power_cost_per_request,
            "total_cost_per_request": total_cost_per_request,
            "cost_per_1k_tokens": cost_per_1k_tokens,
            "hourly_cost": hourly_cost,
            "daily_cost": hourly_cost * 24,
            "monthly_cost": hourly_cost * 24 * 30
        }
    
    def check_hardware_compatibility(self, model_size: str, tokens: int, batch_size: int,
        hardware_type: str, deployment_mode: str) -> Dict[str, any]:
        """Check hardware compatibility and provide recommendations"""
        memory_info = self.calculate_memory_usage(model_size, tokens, batch_size, hardware_type, deployment_mode)
        latency_info = self.calculate_latency(model_size, tokens, batch_size, hardware_type, deployment_mode)
        
        # Compatibility checks
        memory_compatible = memory_info["memory_fits"]
        latency_acceptable = latency_info["total_latency_ms"] < 5000  # 5 seconds threshold
        
        # Performance score (0-100)
        memory_score = max(0, 100 - memory_info["memory_utilization_percent"])
        latency_score = max(0, 100 - (latency_info["total_latency_ms"] / 50))
        performance_score = (memory_score + latency_score) / 2
        
        # Recommendations
        recommendations = []
        if not memory_compatible:
            recommendations.append("Consider using a GPU with more VRAM or reducing batch size")
        if not latency_acceptable:
            recommendations.append("Consider using a more powerful GPU or reducing model size")
        if memory_info["memory_utilization_percent"] > 80:
            recommendations.append("High memory utilization - consider optimization")
        if latency_info["total_latency_ms"] > 2000:
            recommendations.append("High latency - consider model optimization or better hardware")
        
        return {
            "memory_compatible": memory_compatible,
            "latency_acceptable": latency_acceptable,
            "performance_score": performance_score,
            "recommendations": recommendations,
            "memory_utilization_percent": memory_info["memory_utilization_percent"],
            "latency_ms": latency_info["total_latency_ms"]
        }
    
    def calculate_inference_metrics(self, model_size: str, tokens: int, batch_size: int,
        hardware_type: str, deployment_mode: str, 
        requests_per_hour: int = 1) -> Dict[str, any]:
        """Calculate all inference metrics"""
        memory_info = self.calculate_memory_usage(model_size, tokens, batch_size, hardware_type, deployment_mode)
        latency_info = self.calculate_latency(model_size, tokens, batch_size, hardware_type, deployment_mode)
        cost_info = self.calculate_cost(model_size, tokens, batch_size, hardware_type, deployment_mode, requests_per_hour)
        compatibility_info = self.check_hardware_compatibility(model_size, tokens, batch_size, hardware_type, deployment_mode)
        
        return {
            "inputs": {
                "model_size": model_size,
                "tokens": tokens,
                "batch_size": batch_size,
                "hardware_type": hardware_type,
                "deployment_mode": deployment_mode,
                "requests_per_hour": requests_per_hour
            },
            "memory": memory_info,
            "latency": latency_info,
            "cost": cost_info,
            "compatibility": compatibility_info,
            "summary": {
                "total_memory_gb": memory_info["effective_memory_gb"],
                "total_latency_seconds": latency_info["total_latency_seconds"],
                "cost_per_request": cost_info["total_cost_per_request"],
                "tokens_per_second": latency_info["tokens_per_second"],
                "performance_score": compatibility_info["performance_score"]
            }
        }


def main():
    """Example usage of the LLM Inference Calculator"""
    calculator = LLMInferenceCalculator()
    
    # Example 1: 7B model on RTX 4090
    print("=== Example 1: 7B Model on RTX 4090 ===")
    result1 = calculator.calculate_inference_metrics(
        model_size="7B",
        tokens=1024,
        batch_size=1,
        hardware_type="RTX4090",
        deployment_mode="local",
        requests_per_hour=10
    )
    print(json.dumps(result1, indent=2))
    
    # Example 2: 13B model on A100
    print("\n=== Example 2: 13B Model on A100 ===")
    result2 = calculator.calculate_inference_metrics(
        model_size="13B",
        tokens=2048,
        batch_size=4,
        hardware_type="A100",
        deployment_mode="cloud",
        requests_per_hour=100
    )
    print(json.dumps(result2, indent=2))
    
    # Example 3: GPT-4 on H100
    print("\n=== Example 3: GPT-4 on H100 ===")
    result3 = calculator.calculate_inference_metrics(
        model_size="GPT-4",
        tokens=4096,
        batch_size=1,
        hardware_type="H100",
        deployment_mode="cloud",
        requests_per_hour=50
    )
    print(json.dumps(result3, indent=2))


if __name__ == "__main__":
    main() 