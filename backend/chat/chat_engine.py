from datetime import datetime
from typing import List, Optional, Dict, Any, AsyncGenerator
import json
import os
from dataclasses import dataclass, asdict, field
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm.llm_service import llm_service, LLMService


@dataclass
class ChatMessage:
    id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: str
    memory_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatMessage":
        return cls(**data)


class ChatEngine:
    def __init__(self, storage_path: str = "database/chat_history.json"):
        self.storage_path = storage_path
        self.messages: List[ChatMessage] = []
        self.max_history = 1000
        self.llm_service = llm_service
        self._load()
    
    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for m_data in data.get("messages", []):
                        self.messages.append(ChatMessage.from_dict(m_data))
            except Exception:
                pass
    
    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "messages": [m.to_dict() for m in self.messages],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_message(self, role: str, content: str, memory_id: Optional[str] = None) -> ChatMessage:
        import uuid
        message = ChatMessage(
            id=str(uuid.uuid4()),
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            memory_id=memory_id
        )
        self.messages.append(message)
        
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        
        self._save()
        return message
    
    def get_recent(self, limit: int = 50) -> List[ChatMessage]:
        return self.messages[-limit:]
    
    def get_all(self) -> List[ChatMessage]:
        return self.messages
    
    def clear(self):
        self.messages = []
        self._save()
    
    def get_stats(self) -> Dict[str, Any]:
        user_count = sum(1 for m in self.messages if m.role == "user")
        assistant_count = sum(1 for m in self.messages if m.role == "assistant")
        
        return {
            "total_messages": len(self.messages),
            "user_messages": user_count,
            "assistant_messages": assistant_count,
            "first_message_time": self.messages[0].timestamp if self.messages else None,
            "last_message_time": self.messages[-1].timestamp if self.messages else None,
            "llm_configured": self.llm_service.is_configured()
        }
    
    def get_history_for_llm(self, session_id: str = None, limit: int = 10) -> List[Dict[str, str]]:
        """获取用于 LLM 的历史消息格式"""
        messages = self.messages
        if session_id:
            messages = [m for m in messages if m.session_id == session_id]
        
        history = []
        for msg in messages[-limit:]:
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        return history
    
    async def chat(self, message: str, session_id: str = None, 
                   system_prompt: str = None) -> Dict[str, Any]:
        """发送消息并获取 AI 回复"""
        import uuid
        
        # 保存用户消息
        user_msg = self.add_message(
            role="user",
            content=message,
            session_id=session_id
        )
        
        # 获取历史上下文
        history = self.get_history_for_llm(session_id, limit=10)
        
        # 调用 LLM 获取回复
        response = await self.llm_service.chat(message, history, system_prompt)
        
        # 保存 AI 回复
        assistant_msg = self.add_message(
            role="assistant",
            content=response,
            session_id=session_id
        )
        
        return {
            "user_message": user_msg.to_dict(),
            "assistant_message": assistant_msg.to_dict(),
            "response": response,
            "session_id": session_id
        }
    
    async def chat_stream(self, message: str, session_id: str = None,
                          system_prompt: str = None) -> AsyncGenerator[str, None]:
        """流式聊天 - 返回 SSE 格式数据"""
        import uuid
        
        # 保存用户消息
        user_msg = self.add_message(
            role="user",
            content=message,
            session_id=session_id
        )
        
        # 发送用户消息确认
        yield f"data: {json.dumps({'type': 'user_message', 'id': user_msg.id})}\n\n"
        
        # 获取历史上下文
        history = self.get_history_for_llm(session_id, limit=10)
        
        # 流式获取回复
        full_response = ""
        async for chunk in self.llm_service.chat_stream(message, history, system_prompt):
            if chunk.startswith("data: "):
                data_str = chunk[6:]
                if data_str.strip() == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    if "content" in data:
                        full_response += data["content"]
                        yield chunk
                except json.JSONDecodeError:
                    continue
        
        # 保存完整回复
        assistant_msg = self.add_message(
            role="assistant",
            content=full_response,
            session_id=session_id
        )
        
        # 发送完成信号
        yield f"data: {json.dumps({'type': 'done', 'message_id': assistant_msg.id})}\n\n"
        yield "data: [DONE]\n\n"
    
    def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        """获取特定会话的所有消息"""
        return [m for m in self.messages if m.session_id == session_id]
    
    def configure_llm(self, provider: str, api_key: str, model: str = None, 
                      base_url: str = None) -> Dict[str, Any]:
        """配置 LLM 服务"""
        self.llm_service.set_config(provider, api_key, model, base_url)
        return self.llm_service.get_config()
    
    def get_llm_config(self) -> Dict[str, Any]:
        """获取 LLM 配置"""
        return self.llm_service.get_config()
