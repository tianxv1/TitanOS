"""
LLM Service - 支持 DeepSeek API 和流式输出
"""
import httpx
import json
import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator, Callable
from dataclasses import dataclass, field
from datetime import datetime
import os


@dataclass
class LLMConfig:
    """LLM 配置"""
    provider: str = "deepseek"  # deepseek, openai, simulated
    api_key: str = ""
    base_url: str = "https://api.deepseek.com/v1"
    model: str = "deepseek-chat"
    max_tokens: int = 2048
    temperature: float = 0.7
    stream: bool = True


@dataclass
class ChatMessage:
    """聊天消息"""
    role: str  # system, user, assistant
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LLMService:
    """LLM 服务 - 支持 DeepSeek API 和流式输出"""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        # 从环境变量加载配置
        if not self.config.api_key:
            self.config.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not self.config.api_key:
            self.config.api_key = os.getenv("OPENAI_API_KEY", "")
            if self.config.api_key:
                self.config.provider = "openai"
                self.config.base_url = "https://api.openai.com/v1"
                self.config.model = "gpt-3.5-turbo"

    def is_configured(self) -> bool:
        """检查是否已配置 API Key"""
        return bool(self.config.api_key) or self.config.provider == "simulated"

    def set_config(self, provider: str, api_key: str, model: str = None, base_url: str = None):
        """设置 LLM 配置"""
        self.config.provider = provider
        self.config.api_key = api_key
        if model:
            self.config.model = model
        if base_url:
            self.config.base_url = base_url
        elif provider == "deepseek":
            self.config.base_url = "https://api.deepseek.com/v1"
            self.config.model = model or "deepseek-chat"
        elif provider == "openai":
            self.config.base_url = "https://api.openai.com/v1"
            self.config.model = model or "gpt-3.5-turbo"

    def _build_messages(self, user_message: str, history: List[Dict[str, str]], 
                        system_prompt: str = None) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages = []
        
        # 添加系统提示
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({
                "role": "system", 
                "content": "你是 TitanOS 的 AI 助手，一个友好、智能的个人 AI 操作系统。你帮助用户管理记忆、目标和知识。"
            })
        
        # 添加历史消息
        for msg in history[-10:]:  # 最多保留 10 条历史
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_message})
        
        return messages

    async def chat(self, message: str, history: List[Dict[str, str]] = None,
                   system_prompt: str = None) -> str:
        """发送聊天消息并获取回复"""
        if self.config.provider == "simulated":
            return self._simulated_response(message)

        if not self.is_configured():
            return self._simulated_response(message)

        messages = self._build_messages(message, history or [], system_prompt)

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.config.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.config.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "max_tokens": self.config.max_tokens,
                        "temperature": self.config.temperature,
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"LLM API Error: {e}")
                return self._simulated_response(message)

    async def chat_stream(self, message: str, history: List[Dict[str, str]] = None,
                          system_prompt: str = None) -> AsyncGenerator[str, None]:
        """流式聊天 - 返回 SSE 格式的数据"""
        if self.config.provider == "simulated":
            # 模拟流式输出
            response = self._simulated_response(message)
            words = response.split()
            for i, word in enumerate(words):
                yield f"data: {json.dumps({'content': word + (' ' if i < len(words) - 1 else '')})}\n\n"
                await asyncio.sleep(0.05)
            yield "data: [DONE]\n\n"
            return

        if not self.is_configured():
            response = self._simulated_response(message)
            words = response.split()
            for i, word in enumerate(words):
                yield f"data: {json.dumps({'content': word + (' ' if i < len(words) - 1 else '')})}\n\n"
                await asyncio.sleep(0.05)
            yield "data: [DONE]\n\n"
            return

        messages = self._build_messages(message, history or [], system_prompt)

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.config.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.config.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.config.model,
                        "messages": messages,
                        "max_tokens": self.config.max_tokens,
                        "temperature": self.config.temperature,
                        "stream": True
                    }
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                yield "data: [DONE]\n\n"
                                break
                            try:
                                data = json.loads(data_str)
                                if "choices" in data and len(data["choices"]) > 0:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except json.JSONDecodeError:
                                continue
            except Exception as e:
                print(f"LLM Stream API Error: {e}")
                error_msg = f"抱歉，AI 服务暂时不可用。错误: {str(e)}"
                yield f"data: {json.dumps({'content': error_msg})}\n\n"
                yield "data: [DONE]\n\n"

    def _simulated_response(self, message: str) -> str:
        """模拟 AI 回复（当没有配置 API Key 时使用）"""
        message_lower = message.lower()
        
        # 简单的回复逻辑
        if "你好" in message or "hello" in message_lower:
            return "你好！我是 TitanOS AI 助手。我可以帮助你管理记忆、目标和知识。有什么我可以帮助你的吗？"
        elif "记忆" in message or "memory" in message_lower:
            return "我可以帮你管理记忆。你可以告诉我任何想记住的事情，我会帮你保存并建立关联。"
        elif "目标" in message or "goal" in message_lower:
            return "目标管理是 TitanOS 的核心功能。你可以创建目标，我会帮你分解成可执行的步骤。"
        elif "知识" in message or "knowledge" in message_lower:
            return "TitanOS 的知识图谱可以帮你建立知识网络。每次对话都会被分析和关联，形成你的个人知识库。"
        elif "帮助" in message or "help" in message_lower:
            return ("TitanOS 可以帮助你：\n"
                   "1. 💬 智能对话 - 和我聊天，我会记住重要信息\n"
                   "2. 🧠 记忆管理 - 自动保存和关联你的记忆\n"
                   "3. 🎯 目标追踪 - 设定目标，追踪进度\n"
                   "4. 🔗 知识图谱 - 构建你的个人知识网络\n"
                   "5. 👤 数字分身 - 创建你的 AI 分身\n\n"
                   "你想从哪里开始？")
        elif "天气" in message:
            return "抱歉，我目前没有天气查询功能。但我可以帮你记录天气相关的信息，或者讨论其他话题。"
        elif "学习" in message:
            return "学习是成长的关键！你想学习什么？我可以帮你制定学习计划，记录学习笔记，并追踪你的学习进度。"
        elif "谢谢" in message or "感谢" in message:
            return "不客气！很高兴能帮到你。如果还有其他问题，随时可以问我。"
        else:
            return f"我收到了你的消息："{message}"。作为 TitanOS AI 助手，我可以帮你管理记忆、设定目标、构建知识图谱。你想了解哪个功能？"

    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            "provider": self.config.provider,
            "model": self.config.model,
            "base_url": self.config.base_url,
            "is_configured": self.is_configured(),
            "has_api_key": bool(self.config.api_key)
        }


# 全局 LLM 服务实例
llm_service = LLMService()
