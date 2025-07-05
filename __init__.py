"""
DeepSeek LangChain Integration Package
一个简洁高效的DeepSeek API与LangChain集成模块
"""
from .deepseek_llm import DeepSeekLLM, DeepSeekChat, DeepSeekCode, DeepSeekConfig

__version__ = "1.0.0"
__author__ = "DeepSeek Integration Team"
__description__ = "LangChain integration for DeepSeek API"

__all__ = [
    "DeepSeekLLM", 
    "DeepSeekChat", 
    "DeepSeekCode", 
    "DeepSeekConfig"
] 