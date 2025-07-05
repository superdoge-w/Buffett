"""
DeepSeek LLM integration with LangChain

这个模块提供了DeepSeek API与LangChain的集成，支持：
- 标准的LLM调用
- 流式输出
- 多种DeepSeek模型（Chat、Code）
- 完整的错误处理
"""
import os
from typing import Any, Dict, List, Optional, Union
import requests
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import GenerationChunk
from pydantic import Field, SecretStr


# 默认配置
class DeepSeekConfig:
    """DeepSeek配置类"""
    # API配置
    API_KEY: str = "sk-3ad5021f360842faa077e9f3d85103d1"
    BASE_URL: str = "https://api.deepseek.com/v1"
    
    # 模型配置
    DEFAULT_MODEL: str = "deepseek-chat"
    CHAT_MODEL: str = "deepseek-chat"
    CODE_MODEL: str = "deepseek-coder"
    
    # 生成参数
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 1024
    DEFAULT_TOP_P: float = 0.95
    
    @classmethod
    def get_api_key(cls) -> str:
        """获取API密钥"""
        return os.getenv("DEEPSEEK_API_KEY", cls.API_KEY)
    
    @classmethod
    def get_base_url(cls) -> str:
        """获取基础URL"""
        return os.getenv("DEEPSEEK_BASE_URL", cls.BASE_URL)


class DeepSeekLLM(LLM):
    """
    DeepSeek LLM wrapper for LangChain
    
    这个类封装了DeepSeek API，使其能够与LangChain框架无缝集成。
    提供了标准的LLM接口，支持同步和异步调用。
    
    Attributes:
        api_key: DeepSeek API密钥，使用SecretStr保护敏感信息
        base_url: DeepSeek API的基础URL
        model_name: 要使用的模型名称（如deepseek-chat, deepseek-coder）
        temperature: 控制输出随机性的参数，范围0-1，越高越随机
        max_tokens: 生成的最大token数量
        top_p: 核采样参数，控制词汇选择的多样性
    """
    
    # API认证和连接配置
    api_key: SecretStr = Field(default_factory=lambda: SecretStr(""))
    base_url: str = Field(default="https://api.deepseek.com/v1")
    
    # 模型配置
    model_name: str = Field(default="deepseek-chat")
    
    # 生成参数配置
    temperature: float = Field(default=0.7)  # 控制随机性：0=确定性，1=最大随机性
    max_tokens: int = Field(default=1024)    # 限制输出长度
    top_p: float = Field(default=0.95)       # 核采样：保留累积概率top_p的词汇
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        初始化DeepSeek LLM实例
        
        这个构造函数会按以下优先级设置API密钥：
        1. 直接传入的api_key参数
        2. 环境变量DEEPSEEK_API_KEY
        3. 使用默认值（空字符串）
        
        Args:
            api_key: DeepSeek API密钥，可选
            **kwargs: 其他配置参数，如temperature、max_tokens等
        
        Example:
            # 方式1：直接传入API密钥
            llm = DeepSeekLLM(api_key="your-api-key")
            
            # 方式2：使用环境变量
            os.environ["DEEPSEEK_API_KEY"] = "your-api-key"
            llm = DeepSeekLLM()
        """
        # 优先使用传入的API密钥
        if api_key:
            kwargs["api_key"] = SecretStr(api_key)
        # 其次使用环境变量
        elif "DEEPSEEK_API_KEY" in os.environ:
            kwargs["api_key"] = SecretStr(os.environ["DEEPSEEK_API_KEY"])
        
        # 调用父类构造函数
        super().__init__(**kwargs)
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "deepseek"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call DeepSeek API."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key.get_secret_value()}"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": False
        }
        
        # Add stop sequences if provided
        if stop:
            data["stop"] = stop
        
        # Override with any additional parameters
        data.update(kwargs)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                raise ValueError("No response from DeepSeek API")
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"DeepSeek API request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"DeepSeek API error: {e}")
    
    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> GenerationChunk:
        """Stream DeepSeek API response."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key.get_secret_value()}"
        }
        
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "stream": True
        }
        
        if stop:
            data["stop"] = stop
        
        data.update(kwargs)
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str.strip() == '[DONE]':
                            break
                        
                        try:
                            import json
                            data = json.loads(data_str)
                            
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                
                                if content:
                                    chunk = GenerationChunk(text=content)
                                    if run_manager:
                                        run_manager.on_llm_new_token(
                                            token=content,
                                            chunk=chunk,
                                        )
                                    yield chunk
                        except json.JSONDecodeError:
                            continue
                            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"DeepSeek API streaming request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"DeepSeek API streaming error: {e}")
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
        }


class DeepSeekChat(DeepSeekLLM):
    """DeepSeek Chat model specifically for chat completions."""
    
    def __init__(self, **kwargs):
        """Initialize DeepSeek Chat model."""
        kwargs.setdefault("model_name", "deepseek-chat")
        super().__init__(**kwargs)


class DeepSeekCode(DeepSeekLLM):
    """DeepSeek Code model specifically for code generation."""
    
    def __init__(self, **kwargs):
        """Initialize DeepSeek Code model."""
        kwargs.setdefault("model_name", "deepseek-coder")
        super().__init__(**kwargs) 