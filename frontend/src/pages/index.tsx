import { useState } from 'react';

interface Memory {
  id: string;
  content: string;
  importance: number;
  tags: string[];
  timestamp: string;
  access_count: number;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'memory' | 'planner' | 'graph' | 'twin'>('chat');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: '你好！我是 TitanOS，你的个人AI助手。我拥有记忆、推理、规划和学习能力。有什么我可以帮你的吗？',
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [memories, setMemories] = useState<Memory[]>([]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    setTimeout(() => {
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: `收到你的消息: "${input}". 这是一个TitanOS的演示回复。`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <header className="bg-black/30 backdrop-blur-lg border-b border-purple-500/20">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">T</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">TitanOS</h1>
                <p className="text-xs text-purple-400">Personal AI Operating System</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/20 rounded-full">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-green-400 text-sm">System Online</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-black/20 border-b border-purple-500/10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex gap-1">
            {[
              { key: 'chat', label: 'Chat', icon: '💬' },
              { key: 'memory', label: 'Memory', icon: '🧠' },
              { key: 'planner', label: 'Planner', icon: '📋' },
              { key: 'graph', label: 'Knowledge', icon: '🔗' },
              { key: 'twin', label: 'Digital Twin', icon: '👤' }
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key as typeof activeTab)}
                className={`px-4 py-3 text-sm font-medium transition-all flex items-center gap-2 border-b-2 ${
                  activeTab === tab.key
                    ? 'text-purple-400 border-purple-400 bg-purple-500/10'
                    : 'text-gray-400 border-transparent hover:text-white hover:bg-white/5'
                }`}
              >
                <span>{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'chat' && (
          <div className="flex flex-col h-[calc(100vh-220px)]">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-2xl px-4 py-3 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-purple-600 text-white rounded-br-md'
                        : 'bg-gray-800/80 text-gray-100 rounded-bl-md border border-gray-700'
                    }`}
                  >
                    <p className="text-sm">{msg.content}</p>
                    <p className={`text-xs mt-1 ${msg.role === 'user' ? 'text-purple-200' : 'text-gray-500'}`}>
                      {new Date(msg.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-gray-800/50 rounded-2xl border border-gray-700 p-4">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="输入你的问题..."
                  className="flex-1 bg-gray-900/50 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                />
                <button
                  onClick={handleSend}
                  className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-medium rounded-xl hover:opacity-90 transition-opacity"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'memory' && (
          <div className="space-y-6">
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                <p className="text-gray-400 text-sm">Total Memories</p>
                <p className="text-3xl font-bold text-white mt-1">{memories.length || 0}</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                <p className="text-gray-400 text-sm">Important</p>
                <p className="text-3xl font-bold text-purple-400 mt-1">
                  {memories.filter(m => m.importance > 0.7).length || 0}
                </p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                <p className="text-gray-400 text-sm">Recent</p>
                <p className="text-3xl font-bold text-pink-400 mt-1">5</p>
              </div>
              <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700">
                <p className="text-gray-400 text-sm">Tags</p>
                <p className="text-3xl font-bold text-blue-400 mt-1">
                  {new Set(memories.flatMap(m => m.tags)).size || 0}
                </p>
              </div>
            </div>

            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Recent Memories</h2>
              {memories.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No memories yet. Start chatting to create memories!</p>
              ) : (
                <div className="space-y-3">
                  {memories.slice(0, 5).map(memory => (
                    <div key={memory.id} className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
                      <p className="text-white text-sm">{memory.content}</p>
                      <div className="flex items-center gap-4 mt-2">
                        <span className="text-xs text-gray-500">{new Date(memory.timestamp).toLocaleDateString()}</span>
                        <div className="flex gap-1">
                          {memory.tags.map(tag => (
                            <span key={tag} className="px-2 py-0.5 bg-purple-500/20 text-purple-400 text-xs rounded">
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'planner' && (
          <div className="space-y-6">
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Task Planner</h2>
              <p className="text-gray-400">Create plans and track your goals. Powered by TitanOS Planner.</p>
            </div>
          </div>
        )}

        {activeTab === 'graph' && (
          <div className="space-y-6">
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Knowledge Graph</h2>
              <p className="text-gray-400">Visualize entities and relationships. Powered by TitanOS KnowledgeGraph.</p>
            </div>
          </div>
        )}

        {activeTab === 'twin' && (
          <div className="space-y-6">
            <div className="bg-gray-800/50 rounded-xl border border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Digital Twin</h2>
              <p className="text-gray-400">Your personalized AI profile. Learn your style, preferences, and habits.</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
