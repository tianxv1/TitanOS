import { useState, useEffect } from 'react';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface Goal {
  id: number;
  title: string;
  progress: number;
}

interface Memory {
  id: number;
  title: string;
  desc: string;
  tag: string;
  year: string;
  month: string;
}

const API_BASE = 'http://127.0.0.1:8000';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'chat' | 'memory' | 'goals' | 'graph' | 'twin' | 'settings'>('dashboard');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [graphNodes, setGraphNodes] = useState<Array<{id: string, label: string, x: number, y: number, isCenter?: boolean}>>([]);
  const [graphStats, setGraphStats] = useState({ nodes: 0, edges: 0, depth: 0 });
  const [neo4jConfig, setNeo4jConfig] = useState({ uri: 'bolt://localhost:7687', user: 'neo4j', password: '' });
  const [neo4jStatus, setNeo4jStatus] = useState<'disconnected' | 'connecting' | 'connected'>('disconnected');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted) {
      loadGraphData();
    }
  }, [mounted]);

  const loadGraphData = async () => {
    try {
      const res = await fetch(`${API_BASE}/knowledge/graph`);
      if (res.ok) {
        const data = await res.json();
        if (data.nodes && data.nodes.length > 0) {
          setGraphNodes(data.nodes.map((n: any, i: number) => ({
            id: n.id || String(i),
            label: n.label || n.name || 'Node',
            x: n.x || 50 + (i % 5) * 15,
            y: n.y || 30 + Math.floor(i / 5) * 20,
            isCenter: i === 0
          })));
          setGraphStats({ nodes: data.nodes.length, edges: data.edges?.length || 0, depth: 3 });
        } else {
          initDefaultGraph();
        }
      } else {
        initDefaultGraph();
      }
    } catch {
      initDefaultGraph();
    }
  };

  const initDefaultGraph = () => {
    setGraphNodes([
      { id: '1', label: 'TitanOS', x: 45, y: 45, isCenter: true },
      { id: '2', label: 'Memory', x: 30, y: 30 },
      { id: '3', label: 'Knowledge', x: 60, y: 30 },
      { id: '4', label: 'Goals', x: 30, y: 60 },
      { id: '5', label: 'AI Engine', x: 60, y: 60 },
    ]);
    setGraphStats({ nodes: 5, edges: 4, depth: 2 });
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      if (res.ok) {
        const data = await res.json();
        setMessages(prev => [...prev, { role: 'assistant', content: data.response || data.message || '收到消息' }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: `收到: "${input}" - 这是一个演示回复` }]);
      }
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: `收到: "${input}" - 这是一个演示回复` }]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const testNeo4jConnection = async () => {
    setNeo4jStatus('connecting');
    try {
      const res = await fetch(`${API_BASE}/knowledge/configure`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(neo4jConfig)
      });
      if (res.ok) {
        setNeo4jStatus('connected');
      } else {
        setNeo4jStatus('disconnected');
      }
    } catch {
      setNeo4jStatus('disconnected');
    }
  };

  const goals: Goal[] = [
    { id: 1, title: 'Learn Deep Learning', progress: 85 },
    { id: 2, title: 'Build TitanOS v2.0', progress: 60 },
    { id: 3, title: 'Master ML Algorithms', progress: 72 },
    { id: 4, title: 'Create AI Projects', progress: 45 },
  ];

  const memories: Memory[] = [
    { id: 1, title: 'Learned Deep Learning - CNN Model Training', desc: 'Successfully trained CNN model for image classification', tag: 'Learning', year: '2026', month: 'June' },
    { id: 2, title: 'TitanOS v1.0 Released', desc: 'First major release of personal AI operating system', tag: 'Project', year: '2026', month: 'June' },
    { id: 3, title: 'Won Second Prize in AI Competition', desc: 'Competed against 50+ teams and secured top 3 position', tag: 'Achievement', year: '2026', month: 'May' },
    { id: 4, title: 'Started Learning Machine Learning', desc: 'Beginner to intermediate ML concepts and algorithms', tag: 'Learning', year: '2026', month: 'May' },
    { id: 5, title: 'Completed First Python Project', desc: 'Built a data analysis tool from scratch', tag: 'Project', year: '2026', month: 'April' },
  ];

  const skills = [
    { name: 'Memory Growth', percent: 85 },
    { name: 'Knowledge Accumulation', percent: 72 },
    { name: 'Skill Development', percent: 91 },
    { name: 'Goal Completion', percent: 68 },
  ];

  if (!mounted) {
    return null;
  }

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">T</div>
            <div className="logo-text">
              <h1>TitanOS</h1>
              <p>Personal AI Operating System</p>
            </div>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            Dashboard
          </button>
          <button className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveTab('chat')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            Chat
          </button>
          <button className={`nav-item ${activeTab === 'memory' ? 'active' : ''}`} onClick={() => setActiveTab('memory')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Memory
          </button>
          <button className={`nav-item ${activeTab === 'goals' ? 'active' : ''}`} onClick={() => setActiveTab('goals')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            Goals
          </button>
          <button className={`nav-item ${activeTab === 'graph' ? 'active' : ''}`} onClick={() => setActiveTab('graph')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            Knowledge Graph
          </button>
          <button className={`nav-item ${activeTab === 'twin' ? 'active' : ''}`} onClick={() => setActiveTab('twin')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Digital Twin
          </button>
          <button className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`} onClick={() => setActiveTab('settings')}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Settings
          </button>
        </nav>

        <div className="sidebar-footer">
          <div className="status-indicator">
            <div className="status-dot"></div>
            <span className="status-text">System Online</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <div id="dashboard" className={`tab-content ${activeTab === 'dashboard' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Dashboard</h2>
            <p>Your personal AI growth metrics at a glance</p>
          </div>
          <div className="content-body">
            <div className="dashboard-grid">
              <div className="stat-card">
                <div className="stat-label">Total Memories</div>
                <div className="stat-value">{memories.length * 247}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Knowledge Nodes</div>
                <div className="stat-value accent">{graphStats.nodes * 66}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Active Goals</div>
                <div className="stat-value primary">{goals.length}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">Growth Score</div>
                <div className="stat-value">78</div>
              </div>
            </div>

            <div className="growth-section">
              <div className="circular-progress">
                <div className="progress-ring">
                  <svg width="200" height="200" viewBox="0 0 200 200">
                    <defs>
                      <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#7C3AED"/>
                        <stop offset="100%" stopColor="#22D3EE"/>
                      </linearGradient>
                    </defs>
                    <circle className="bg" cx="100" cy="100" r="85"/>
                    <circle className="progress" cx="100" cy="100" r="85" strokeDasharray="534" strokeDashoffset="117"/>
                  </svg>
                  <div className="progress-text">
                    <div className="progress-number">78</div>
                    <div className="progress-label">Growth</div>
                  </div>
                </div>
                <h3>Overall Growth Score</h3>
                <p>Expert Level - Keep pushing!</p>
              </div>

              <div className="progress-bars">
                <h3>Skill Progress</h3>
                {skills.map((skill, idx) => (
                  <div className="progress-item" key={idx}>
                    <div className="progress-header">
                      <span className="progress-title">{skill.name}</span>
                      <span className="progress-percent">{skill.percent}%</span>
                    </div>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{width: `${skill.percent}%`}}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div id="chat" className={`tab-content ${activeTab === 'chat' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Chat</h2>
            <p>Interact with your AI assistant</p>
          </div>
          <div className="content-body">
            <div className="chat-container">
              <div className="chat-messages">
                {messages.length === 0 ? (
                  <div className="message assistant">
                    <div className="message-avatar">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div className="message-content">
                      <div className="message-text">你好！我是 TitanOS，你的个人 AI 助手。我拥有记忆、推理、规划和学习能力。有什么我可以帮你的吗？</div>
                      <div className="message-time">09:30:00</div>
                    </div>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                      <div className="message-avatar">
                        {msg.role === 'assistant' ? (
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                          </svg>
                        ) : (
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                        )}
                      </div>
                      <div className="message-content">
                        <div className="message-text">{msg.content}</div>
                        <div className="message-time">{msg.role === 'user' ? '10:00:00' : '10:00:01'}</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
              <div className="chat-input">
                <div className="chat-input-form">
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="输入你的问题..."
                    autoComplete="off"
                  />
                  <button onClick={handleSend}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                    Send
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div id="memory" className={`tab-content ${activeTab === 'memory' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Memory Timeline</h2>
            <p>Your life events organized chronologically</p>
          </div>
          <div className="content-body">
            <div className="search-section">
              <div className="search-section-inner">
                <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="search-title">Semantic Search (Powered by Vector DB)</span>
              </div>
              <div className="search-input-row">
                <input type="text" className="search-input" placeholder="Search memories with natural language... (e.g., 'What did I learn about Python?')" />
                <button className="btn-primary">Search</button>
                <button className="btn-secondary">Sync</button>
              </div>
              <div className="vector-db-status">Vector DB: Ready</div>
            </div>
            <div className="timeline">
              <div className="timeline-year">
                <div className="timeline-year-header">2026</div>
                {['June', 'May', 'April'].map(month => (
                  <div className="timeline-month" key={month}>
                    <div className="timeline-month-header">{month}</div>
                    {memories.filter(m => m.month === month).map(memory => (
                      <div className="timeline-item" key={memory.id}>
                        <div className="timeline-item-title">{memory.title}</div>
                        <div className="timeline-item-desc">{memory.desc}</div>
                        <span className="timeline-item-tag">{memory.tag}</span>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div id="goals" className={`tab-content ${activeTab === 'goals' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Goal Tree</h2>
            <p>Track your objectives and milestones</p>
          </div>
          <div className="content-body">
            <div className="goals-container">
              <div className="goal-tree">
                {goals.map(goal => (
                  <div className="goal-item" key={goal.id}>
                    <div className="goal-header">
                      <span className="goal-title">{goal.title}</span>
                      <span className="goal-progress">{goal.progress}%</span>
                    </div>
                    <div className="goal-bar">
                      <div className="goal-bar-fill" style={{width: `${goal.progress}%`}}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div id="graph" className={`tab-content ${activeTab === 'graph' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Knowledge Graph</h2>
            <p>Visualize entities and relationships</p>
          </div>
          <div className="content-body">
            <div className="knowledge-graph-container">
              {graphNodes.map(node => (
                <div
                  key={node.id}
                  className={`graph-node ${node.isCenter ? 'center' : ''}`}
                  style={{ left: `${node.x}%`, top: `${node.y}%` }}
                >
                  {node.label}
                </div>
              ))}
            </div>
            <div className="graph-stats">
              <div className="graph-stat">
                <div className="graph-stat-value">{graphStats.nodes}</div>
                <div className="graph-stat-label">Nodes</div>
              </div>
              <div className="graph-stat">
                <div className="graph-stat-value">{graphStats.edges}</div>
                <div className="graph-stat-label">Edges</div>
              </div>
              <div className="graph-stat">
                <div className="graph-stat-value">{graphStats.depth}</div>
                <div className="graph-stat-label">Depth</div>
              </div>
            </div>
          </div>
        </div>

        <div id="twin" className={`tab-content ${activeTab === 'twin' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Digital Twin</h2>
            <p>Your personalized AI profile</p>
          </div>
          <div className="content-body">
            <div className="twin-grid">
              <div className="twin-card">
                <h3>Communication Style</h3>
                <div className="style-item">
                  <span className="style-name">Formality</span>
                  <span className="style-value">Balanced</span>
                </div>
                <div className="style-item">
                  <span className="style-name">Verbosity</span>
                  <span className="style-value">Moderate</span>
                </div>
                <div className="style-item">
                  <span className="style-name">Technical Depth</span>
                  <span className="style-value">High</span>
                </div>
              </div>
              <div className="twin-card">
                <h3>Personality Traits</h3>
                <div className="persona-grid">
                  <div className="persona-item">
                    <span className="persona-name">Curiosity</span>
                    <span className="persona-value">92</span>
                    <div className="persona-bar"><div className="persona-bar-fill" style={{width: '92%'}}></div></div>
                  </div>
                  <div className="persona-item">
                    <span className="persona-name">Logic</span>
                    <span className="persona-value">88</span>
                    <div className="persona-bar"><div className="persona-bar-fill" style={{width: '88%'}}></div></div>
                  </div>
                  <div className="persona-item">
                    <span className="persona-name">Creativity</span>
                    <span className="persona-value">76</span>
                    <div className="persona-bar"><div className="persona-bar-fill" style={{width: '76%'}}></div></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div id="settings" className={`tab-content ${activeTab === 'settings' ? 'active' : ''}`}>
          <div className="content-header">
            <h2>Settings</h2>
            <p>Configure your TitanOS preferences</p>
          </div>
          <div className="content-body">
            <div className="config-section">
              <h3>Neo4j Connection</h3>
              <div className="config-row">
                <div className="config-field">
                  <label>URI</label>
                  <input
                    type="text"
                    value={neo4jConfig.uri}
                    onChange={(e) => setNeo4jConfig({...neo4jConfig, uri: e.target.value})}
                    placeholder="bolt://localhost:7687"
                  />
                </div>
                <div className="config-field">
                  <label>Username</label>
                  <input
                    type="text"
                    value={neo4jConfig.user}
                    onChange={(e) => setNeo4jConfig({...neo4jConfig, user: e.target.value})}
                    placeholder="neo4j"
                  />
                </div>
              </div>
              <div className="config-row">
                <div className="config-field">
                  <label>Password</label>
                  <input
                    type="password"
                    value={neo4jConfig.password}
                    onChange={(e) => setNeo4jConfig({...neo4jConfig, password: e.target.value})}
                    placeholder="Enter password"
                  />
                </div>
                <div className="config-field">
                  <label>Status</label>
                  <div className={`status-badge ${neo4jStatus}`}>
                    <div className="status-dot" style={{display: neo4jStatus === 'connected' ? 'block' : 'none'}}></div>
                    {neo4jStatus === 'connected' ? 'Connected' : neo4jStatus === 'connecting' ? 'Connecting...' : 'Disconnected'}
                  </div>
                </div>
              </div>
              <div className="config-actions">
                <button className="btn-primary" onClick={testNeo4jConnection}>Test Connection</button>
                <button className="btn-secondary" onClick={() => setNeo4jStatus('connected')}>Enable Knowledge Graph</button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}