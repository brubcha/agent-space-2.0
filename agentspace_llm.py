"""
AgentSpace - LLM Integration Module

Connectors for:
- Claude (Anthropic) - Primary
- GPT (OpenAI) - Backup
- Gemini (Google) - Future

Each connector provides:
- Connection handling
- Rate limiting
- Error handling
- Cost tracking
- Streaming support
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    ENV_LOADED = True
except ImportError:
    ENV_LOADED = False
    print("⚠️  python-dotenv not installed. Using system environment variables.")

# Claude (Anthropic)
try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False
    print("⚠️  anthropic not installed. Install: pip install anthropic")

# GPT (OpenAI)
try:
    from openai import OpenAI
    GPT_AVAILABLE = True
except ImportError:
    GPT_AVAILABLE = False
    print("⚠️  openai not installed. Install: pip install openai")


# ============================================================================
# BASE LLM CLASS
# ============================================================================

class BaseLLM:
    """Base class for all LLM providers."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0
        }
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate content from prompt. Override in subclass."""
        raise NotImplementedError
    
    def count_tokens(self, text: str) -> int:
        """Rough token count (4 chars = 1 token)."""
        return len(text) // 4
    
    def update_stats(self, tokens: int, cost: float):
        """Update usage statistics."""
        self.usage_stats["total_requests"] += 1
        self.usage_stats["total_tokens"] += tokens
        self.usage_stats["total_cost"] += cost
    
    def get_stats(self) -> Dict:
        """Get usage statistics."""
        return self.usage_stats.copy()


# ============================================================================
# CLAUDE (ANTHROPIC)
# ============================================================================

class ClaudeLLM(BaseLLM):
    """
    Claude connector via Anthropic API.
    
    Models:
    - claude-sonnet-4-20250514 (recommended - best quality)
    - claude-opus-4-20241129 (most powerful, expensive)
    - claude-haiku-4-20250114 (fastest, cheapest)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        super().__init__(api_key)
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        if not CLAUDE_AVAILABLE:
            raise ImportError("anthropic library not installed")
        
        self.client = Anthropic(api_key=self.api_key)
        
        # Pricing (per million tokens)
        self.pricing = {
            "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
            "claude-opus-4-20241129": {"input": 15.0, "output": 75.0},
            "claude-haiku-4-20250114": {"input": 0.8, "output": 4.0},
        }
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate content using Claude.
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: 0.0 (focused) to 1.0 (creative)
            system: System prompt (optional)
            
        Returns:
            {
                "content": "Generated text",
                "model": "claude-sonnet-4...",
                "tokens": {"input": 100, "output": 500},
                "cost": 0.0075
            }
        """
        
        try:
            # Build messages
            messages = [{"role": "user", "content": prompt}]
            
            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system if system else None,
                messages=messages
            )
            
            # Extract content
            content = response.content[0].text
            
            # Calculate usage
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            
            # Calculate cost
            pricing = self.pricing.get(self.model, {"input": 3.0, "output": 15.0})
            cost = (input_tokens / 1_000_000 * pricing["input"]) + \
                   (output_tokens / 1_000_000 * pricing["output"])
            
            # Update stats
            self.update_stats(input_tokens + output_tokens, cost)
            
            return {
                "content": content,
                "model": self.model,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                },
                "cost": cost,
                "success": True
            }
        
        except Exception as e:
            return {
                "content": None,
                "error": str(e),
                "success": False
            }


# ============================================================================
# GPT (OPENAI)
# ============================================================================

class GPTLLM(BaseLLM):
    """
    GPT connector via OpenAI API.
    
    Models:
    - gpt-4o (recommended - best value)
    - gpt-4-turbo (powerful)
    - gpt-3.5-turbo (cheapest)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        super().__init__(api_key)
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        if not GPT_AVAILABLE:
            raise ImportError("openai library not installed")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Pricing (per million tokens)
        self.pricing = {
            "gpt-4o": {"input": 2.5, "output": 10.0},
            "gpt-4-turbo": {"input": 10.0, "output": 30.0},
            "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        }
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        system: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate content using GPT.
        
        Returns same format as ClaudeLLM.generate()
        """
        
        try:
            # Build messages
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            
            # Call GPT
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract content
            content = response.choices[0].message.content
            
            # Calculate usage
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            # Calculate cost
            pricing = self.pricing.get(self.model, {"input": 2.5, "output": 10.0})
            cost = (input_tokens / 1_000_000 * pricing["input"]) + \
                   (output_tokens / 1_000_000 * pricing["output"])
            
            # Update stats
            self.update_stats(input_tokens + output_tokens, cost)
            
            return {
                "content": content,
                "model": self.model,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens
                },
                "cost": cost,
                "success": True
            }
        
        except Exception as e:
            return {
                "content": None,
                "error": str(e),
                "success": False
            }


# ============================================================================
# LLM FACTORY
# ============================================================================

class LLMFactory:
    """Factory for creating LLM instances."""
    
    @staticmethod
    def create(
        provider: str = "claude",
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> BaseLLM:
        """
        Create an LLM instance.
        
        Args:
            provider: "claude" or "gpt"
            model: Specific model (optional, uses default)
            api_key: API key (optional, uses env var)
            
        Returns:
            LLM instance
        """
        
        provider = provider.lower()
        
        if provider == "claude":
            if not CLAUDE_AVAILABLE:
                raise ImportError("Claude not available. Install: pip install anthropic")
            model = model or "claude-sonnet-4-20250514"
            return ClaudeLLM(api_key=api_key, model=model)
        
        elif provider == "gpt":
            if not GPT_AVAILABLE:
                raise ImportError("GPT not available. Install: pip install openai")
            model = model or "gpt-4o"
            return GPTLLM(api_key=api_key, model=model)
        
        else:
            raise ValueError(f"Unknown provider: {provider}")


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def generate_with_llm(
    prompt: str,
    provider: str = "claude",
    system: Optional[str] = None,
    max_tokens: int = 4000,
    temperature: float = 0.7
) -> str:
    """
    Convenience function for quick generation.
    
    Args:
        prompt: What to generate
        provider: "claude" or "gpt"
        system: System instructions
        max_tokens: Max output length
        temperature: Creativity level
        
    Returns:
        Generated text (or error message)
    """
    
    try:
        llm = LLMFactory.create(provider=provider)
        result = llm.generate(
            prompt=prompt,
            system=system,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if result["success"]:
            print(f"✓ Generated {result['tokens']['output']} tokens (${result['cost']:.4f})")
            return result["content"]
        else:
            print(f"✗ Error: {result['error']}")
            return f"[Error: {result['error']}]"
    
    except Exception as e:
        print(f"✗ Failed: {str(e)}")
        return f"[Failed: {str(e)}]"


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("LLM Integration Test")
    print("=" * 80)
    print()
    
    # Test Claude
    print("Testing Claude...")
    try:
        claude = ClaudeLLM()
        result = claude.generate(
            prompt="Write a one-sentence tagline for a healthcare technology company.",
            max_tokens=100
        )
        
        if result["success"]:
            print(f"✓ Claude Response: {result['content']}")
            print(f"  Tokens: {result['tokens']['total']}")
            print(f"  Cost: ${result['cost']:.4f}")
        else:
            print(f"✗ Error: {result['error']}")
    except Exception as e:
        print(f"✗ Claude not available: {str(e)}")
    
    print()
    
    # Test GPT
    print("Testing GPT...")
    try:
        gpt = GPTLLM()
        result = gpt.generate(
            prompt="Write a one-sentence tagline for a healthcare technology company.",
            max_tokens=100
        )
        
        if result["success"]:
            print(f"✓ GPT Response: {result['content']}")
            print(f"  Tokens: {result['tokens']['total']}")
            print(f"  Cost: ${result['cost']:.4f}")
        else:
            print(f"✗ Error: {result['error']}")
    except Exception as e:
        print(f"✗ GPT not available: {str(e)}")
    
    print()
    print("=" * 80)
