    Start new chat

Starred

    Handling NoneType Error in Live Game Play-by-Play Data

Recents

Optimizing Ollama Token Length for High-End GPUs
(New chat)
SSH Port Forwarding Functions
Troubleshooting a non-working script
Terminal-based Ollama Chat Program
Running Ollama Models on 0.0.0.0:11434
Removing and Adding SSH Keys

    PowerShell SSH Alias Setup

View all
Free plan
Help & support
KH
KH

how do i increase the ollama token length through open-webui and also give me an approximation or guide to guage how to increase and decrease this value such that I make full use of my graphics card (4090).  I understand different models may warrant different input structures (ollama is the backend runner I'm using).  So give me a good way to iterate while maximizing token length, ideally, id want this to be largest it can be always

Let me help you optimize your token length settings for Ollama with the OpenWebUI interface.

To modify the token length (context window) in OpenWebUI:

    Navigate to Model Settings in OpenWebUI
    Find the "Context Length" or "n_ctx" parameter
    Adjust the value while keeping in mind your GPU constraints

For an RTX 4090 with 24GB VRAM, here's a systematic approach to finding your optimal token length:

    Start with a baseline:

    For 7B models: Try 8192 tokens initially
    For 13B models: Start with 6144 tokens
    For 34B+ models: Begin with 4096 tokens

    Iteration process:

1. Increase token length by 2048
2. Run a long conversation or generation task
3. Monitor GPU memory usage (using nvidia-smi)
4. If stable, increase again
5. If you get OOM errors, decrease by 1024
6. Fine-tune in smaller increments (512 or 256) near the limit

Rough guidelines for RTX 4090:

    7B models: Can often handle 16K-32K tokens
    13B models: Usually stable at 8K-16K tokens
    34B models: Typically 4K-8K tokens
    70B models: Usually limited to 4K-6K tokens

Key things to monitor:

    GPU memory usage should stay below ~22GB
    Watch for slowdowns in response time
    Check for stability over multiple generations
    Temperature of your GPU

The exact numbers will vary based on:

    Model quantization (4-bit, 8-bit, etc.)
    Other applications running
    System RAM available
    Specific model architecture

Would you like me to provide more specific guidance for any particular model you're using?
KH

why can smaller models handle higher token sizes?  wtf?

Ah, let me explain this! It's actually quite logical:

Each model parameter (weight) needs to interact with the input tokens during processing. So with larger models, you have:

    More parameters that need to process each token
    More memory needed per token for attention calculations
    Larger intermediate activations for each layer

Think of it like this: A 7B model might need X memory per token, but a 70B model needs roughly 10X memory per token because it has 10 times more parameters all needing to process that same token.

The memory usage grows quadratically with context length (due to attention mechanisms) AND linearly with model size. So if you have a fixed GPU memory budget (24GB for your 4090), you have to balance between:

    Model size (parameters)
    Context length (tokens)

It's like trying to fit people (tokens) into rooms (GPU memory):

    A small hotel (7B model) with simple rooms can fit more people
    A luxury hotel (70B model) with massive suites fits fewer people because each person needs way more space

This is why you often see smaller models being used for long-context tasks - they can handle more tokens with their smaller memory footprint per token. Newer architectures like Mamba and state-space models are trying to solve this quadratic scaling problem, but for traditional transformer models, this tradeoff remains.
KH

so semantically yes they can handle higher token sizes because they themselves are smaller but stick to the essence of what I'm trying to do - is that useful?  Realistically I want a useful model, not a shitty model that has a massive token size it can't perform on

Ah, now I better understand what you're getting at - you're absolutely right. While smaller models can technically handle larger token sizes, that's not really the point if they can't do useful work with those tokens.

For actual practical use, you'd typically want to:

    First choose a model that's actually capable of the task you need (like a 13B or larger model)
    Then maximize the context length within the constraints of that model

So if you're using something like Mixtral 8x7B or CodeLlama 34B for real work, you'd probably want to:

    Start with 8K context
    Push up gradually (8K → 16K → etc.)
    Stop when you either:
        Hit GPU memory limits
        See significant performance degradation
        Get OOM errors

The key is finding the sweet spot where you have enough context to be useful while maintaining model performance. Having a 70K context window on a tiny model that can't coherently process that much information isn't actually helpful.

Would you like to discuss optimizing for a specific model you're planning to use? That way we can focus on practical limits that would actually be useful for your work.
KH

is there an average of range of coefficients i can use to approximate tokens to words?  that should be a metric for every model in my opinion.  is there a tool that performs all these approximations so I don't have to iterate uselessly?

For token-to-word ratios, here's a general approximation:

English text typically converts at:

    4 characters ≈ 1 token
    0.75 tokens ≈ 1 word
    Or roughly 1.3-1.5 words per token

But this varies significantly based on:

    Language (Japanese/Chinese use fewer tokens per word)
    Technical content (code, scientific notation)
    Special characters/formatting

For practical estimation:

python

# Quick approximation
words = tokens * 0.75
# or
tokens_needed = words * 1.3

As for automated tools for finding optimal context lengths - there isn't a comprehensive one I know of that works across different models and hardware. This is partly because optimal settings depend on:

    GPU memory/specifications
    Model architecture
    Use case requirements
    System RAM
    Other running processes

However, for Ollama specifically, you could monitor memory usage programmatically using something like:

python

import subprocess
import json

def get_gpu_memory():
    result = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,nounits,noheader'])
    return int(result)

def find_max_context(model_name, start_ctx=4096, step=2048):
    # Test increasing context sizes until OOM
    current_ctx = start_ctx
    while True:
        try:
            # Test model with current context
            # Add your Ollama API call here
            if get_gpu_memory() > MEMORY_THRESHOLD:
                return current_ctx - step
            current_ctx += step
        except:
            return current_ctx - step

Would you like me to expand on building a testing tool for your specific setup?
KH

i'd rather take all the components that you listed, and grab them in this program.  that is information we can use in our approximator.  thus, if we grab GPU, model architecture, system RAM, case requirements -> generate me a script that helps me by printing me a range of possible context values and how to pick

I'll create a script that analyzes your system and provides context window recommendations based on actual hardware and model specs.

This script provides:

    System Analysis:
        GPU memory and model
        Available system RAM
        Current memory usage
    Model-specific calculations:
        Memory per token estimates
        Adjustments for quantization (4-bit, 8-bit, etc.)
        Scaling based on model size
    Three recommendation tiers:
        Conservative: Safe starting point
        Balanced: Optimal for most uses
        Aggressive: Maximum theoretical limit

To use it:

    Install requirements: pip install psutil
    Run the script: python context_analyzer.py

The script makes educated guesses based on known parameters and hardware limits. Would you like me to adjust any of the estimation parameters or add additional features?
Claude can make mistakes. Please double-check responses.


Context Window Size Analyzer
import subprocess
import psutil
import os
import json
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

@dataclass
class ModelSpecs:
    name: str
    parameters: int  # in billions
    quantization: str
    architecture: str = "transformer"  # default to transformer

@dataclass
class SystemSpecs:
    gpu_memory: int  # in MB
    gpu_name: str
    system_ram: int  # in GB
    free_ram: int  # in GB

def get_gpu_info() -> Tuple[int, str]:
    try:
        result = subprocess.check_output([
            'nvidia-smi', 
            '--query-gpu=memory.total,name', 
            '--format=csv,noheader,nounits'
        ]).decode()
        memory, name = result.strip().split(',')
        return int(memory), name.strip()
    except:
        return 0, "No NVIDIA GPU found"

def get_system_specs() -> SystemSpecs:
    gpu_memory, gpu_name = get_gpu_info()
    ram = psutil.virtual_memory()
    return SystemSpecs(
        gpu_memory=gpu_memory,
        gpu_name=gpu_name,
        system_ram=ram.total // (1024**3),
        free_ram=ram.available // (1024**3)
    )

def estimate_token_memory(model: ModelSpecs) -> float:
    """Estimate memory needed per token in MB"""
    base_memory = {
        "4-bit": 0.5,
        "8-bit": 1,
        "16-bit": 2,
        "32-bit": 4
    }
    
    # Adjust for model size
    memory_per_token = base_memory.get(model.quantization, 2) * (model.parameters / 7)
    
    # Add overhead for attention mechanisms
    if model.architecture.lower() == "transformer":
        memory_per_token *= 1.2  # 20% overhead for attention
    
    return memory_per_token

def suggest_context_window(system: SystemSpecs, model: ModelSpecs) -> Dict[str, int]:
    # Reserve some GPU memory for system overhead (10%)
    available_memory = system.gpu_memory * 0.9
    
    # Calculate memory per token
    mem_per_token = estimate_token_memory(model)
    
    # Calculate theoretical max tokens (considering quadratic attention)
    # Using a simplified square root calculation for attention memory scaling
    max_tokens = int((available_memory / mem_per_token) ** 0.5)
    
    # Provide conservative and aggressive estimates
    return {
        "conservative": max(2048, (max_tokens // 2048) * 2048),  # Round down to nearest 2048
        "balanced": max(2048, ((max_tokens * 3 // 4) // 2048) * 2048),
        "aggressive": max(2048, (max_tokens // 2048) * 2048)
    }

def main():
    # Get system specifications
    system = get_system_specs()
    
    print(f"\n=== System Specifications ===")
    print(f"GPU: {system.gpu_name}")
    print(f"GPU Memory: {system.gpu_memory}MB")
    print(f"System RAM: {system.system_ram}GB")
    print(f"Free RAM: {system.free_ram}GB")
    
    # Example models with different sizes
    models = {
        "7B": ModelSpecs("7B", 7, "4-bit"),
        "13B": ModelSpecs("13B", 13, "4-bit"),
        "34B": ModelSpecs("34B", 34, "4-bit"),
        "70B": ModelSpecs("70B", 70, "4-bit")
    }
    
    print("\n=== Recommended Context Windows ===")
    print("\nTokens (→ Approximate words)")
    for model_name, model in models.items():
        suggestions = suggest_context_window(system, model)
        print(f"\n{model_name} Model ({model.quantization}):")
        print(f"  Conservative: {suggestions['conservative']:,} tokens (≈{int(suggestions['conservative']*0.75):,} words)")
        print(f"  Balanced:     {suggestions['balanced']:,} tokens (≈{int(suggestions['balanced']*0.75):,} words)")
        print(f"  Aggressive:   {suggestions['aggressive']:,} tokens (≈{int(suggestions['aggressive']*0.75):,} words)")
    
    print("\nUsage Guidelines:")
    print("1. Start with Conservative setting for stability")
    print("2. Move to Balanced if no issues occur")
    print("3. Try Aggressive only if your specific use case requires it")
    print("4. Monitor GPU memory usage and performance")
    print("\nNote: Actual usable context may vary based on:")
    print("- Model architecture specifics")
    print("- Other running applications")
    print("- System temperature and stability")
    print("- Specific model implementation")

if __name__ == "__main__":
    main()
Last edited just now
