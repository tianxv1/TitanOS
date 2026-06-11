'use client';

import { useEffect, useState, useRef } from 'react';
import { Send, Bot, User as UserIcon, RefreshCw } from 'lucide-react';
import api from '@/lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatHistory = async () => {
    try {
      const history = await api.getChatHistory(50);
      if (history.messages) {
        setMessages(
          history.messages.map((msg: any, index: number) => ({
            id: `msg-${index}`,
            role: msg.role,
            content: msg.content,
            timestamp: msg.timestamp || new Date().toISOString()
          }))
        );
      }
    } catch (err) {
      console.error('Failed to load chat history:', err);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: `msg-${Date.now()}-user`,
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setError(null);

    try {
      const response = await api.sendChat(userMessage.content);
      const assistantMessage: Message = {
        id: `msg-${Date.now()}-assistant`,
        role: 'assistant',
        content: response.response || response.message || 'I received your message.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Failed to send message:', err);
      setError('Failed to send message. Please try again.');
      const errorMessage: Message = {
        id: `msg-${Date.now()}-error`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Chat</h1>
        <p>Talk with your AI assistant. Conversations are saved to memory automatically.</p>
      </div>

      <div className="chat-container card" style={{ padding: 0 }}>
        <div
          className="chat-messages"
          style={{ background: 'var(--bg-tertiary)', borderRadius: '16px 16px 0 0' }}
        >
          {messages.length === 0 && (
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                color: 'var(--text-muted)'
              }}
            >
              <Bot size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
              <p style={{ fontSize: '16px', marginBottom: '8px' }}>
                Start a conversation with TitanOS
              </p>
              <p style={{ fontSize: '13px' }}>
                Your conversations will be saved to memory automatically.
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={`chat-message ${message.role}`}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                {message.role === 'assistant' ? (
                  <Bot size={20} style={{ flexShrink: 0, marginTop: '2px' }} />
                ) : (
                  <UserIcon size={20} style={{ flexShrink: 0, marginTop: '2px' }} />
                )}
                <div style={{ flex: 1 }}>
                  <div>{message.content}</div>
                  <div
                    style={{
                      fontSize: '11px',
                      marginTop: '8px',
                      opacity: 0.7
                    }}
                  >
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-message assistant">
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Bot size={20} style={{ flexShrink: 0 }} />
                <div className="spinner" style={{ width: '16px', height: '16px' }} />
                <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                  Thinking...
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <input
              type="text"
              className="chat-input"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <button
              className="chat-send-btn"
              onClick={handleSend}
              disabled={loading || !input.trim()}
            >
              <Send size={20} />
            </button>
            <button
              className="btn btn-icon btn-secondary"
              onClick={loadChatHistory}
              title="Refresh chat history"
            >
              <RefreshCw size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}