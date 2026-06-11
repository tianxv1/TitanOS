"""
LLM 模块 - 支持 DeepSeek、OpenAI 等多种 LLM 提供商
"""
from .llm_service import LLMService, LLMConfig, ChatMessage, llm_service

__all__ = ["LLMService", "LLMConfig", "ChatMessage", "llm_service"]
