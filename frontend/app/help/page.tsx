'use client';

import { useState } from 'react';
import { Book, ExternalLink, MessageSquare, Brain, GitBranch, Database } from 'lucide-react';

interface HelpTopic {
  id: string;
  title: string;
  icon: any;
  description: string;
  content: string;
}

export default function HelpPage() {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);

  const topics: HelpTopic[] = [
    {
      id: 'chat',
      title: 'Chat',
      icon: MessageSquare,
      description: 'Learn how to interact with TitanOS through chat',
      content: `
## Chat with TitanOS

TitanOS supports natural language conversations. Here's how to get started:

1. **Start a Conversation**: Click on the Chat tab in the sidebar
2. **Send Messages**: Type your message and press Enter or click Send
3. **Memory Integration**: All conversations are automatically saved to memory
4. **Context Awareness**: TitanOS remembers your previous conversations

### Tips
- Be specific in your questions
- Ask follow-up questions for deeper understanding
- Use clear and concise language
      `
    },
    {
      id: 'memory',
      title: 'Memory System',
      icon: Brain,
      description: 'Understand how TitanOS stores and retrieves memories',
      content: `
## Memory System

TitanOS has a sophisticated multi-tier memory system:

### Memory Types
- **Episodic Memory**: Stores specific experiences and events
- **Semantic Memory**: Stores general knowledge and facts
- **Procedural Memory**: Stores skills and how to do things

### Vector Search
The memory system supports semantic search powered by vector databases:
- Qdrant
- Weaviate
- Pinecone
- In-Memory (default)

### Accessing Memories
1. Go to the Memory page
2. Use natural language to search (e.g., "What did I learn about Python?")
3. View your memory timeline chronologically
      `
    },
    {
      id: 'knowledge-graph',
      title: 'Knowledge Graph',
      icon: GitBranch,
      description: 'Visualize relationships between entities',
      content: `
## Knowledge Graph

The Knowledge Graph feature (v2.0) provides advanced entity relationship visualization:

### Features
- **Entity Management**: Create and manage entities
- **Relationship Tracking**: Define relationships between entities
- **Path Finding**: Discover connections between entities
- **LLM Integration**: Automatically extract entities from text

### Neo4j Integration
Connect to Neo4j for scalable graph storage:
1. Go to Settings
2. Configure your Neo4j connection
3. Sync your local data to Neo4j

### Using LLM Analysis
1. Go to Knowledge Graph page
2. Enter text in the LLM Text Analysis box
3. TitanOS will extract entities and relationships automatically
      `
    },
    {
      id: 'vector-db',
      title: 'Vector Database',
      icon: Database,
      description: 'Configure semantic search with vector databases',
      content: `
## Vector Database

TitanOS supports multiple vector database providers for semantic search:

### Available Providers
- **In-Memory**: Default, no external dependencies
- **Qdrant**: High-performance vector database
- **Weaviate**: Cloud-native vector search
- **Pinecone**: Managed vector database

### Configuration
1. Go to Settings
2. Select your preferred Vector DB provider
3. Configure connection settings
4. Click "Sync to Vector DB" to migrate data

### Semantic Search
Use natural language to search your memories:
- "What did I learn about machine learning?"
- "Find my discussions about Python"
- "Show me content related to my projects"
      `
    }
  ];

  const currentTopic = topics.find(t => t.id === selectedTopic);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Help Center</h1>
        <p>Learn how to use TitanOS features effectively.</p>
      </div>

      <div className="grid grid-2">
        <div>
          <div className="card-header" style={{ marginBottom: '16px' }}>
            <h3 className="card-title">Topics</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {topics.map((topic) => {
              const Icon = topic.icon;
              return (
                <div
                  key={topic.id}
                  className="card"
                  style={{
                    cursor: 'pointer',
                    borderColor: selectedTopic === topic.id ? 'var(--accent-purple)' : 'var(--border-color)',
                    padding: '16px'
                  }}
                  onClick={() => setSelectedTopic(topic.id)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div
                      className="card-icon"
                      style={{
                        background: selectedTopic === topic.id
                          ? 'var(--gradient-purple-cyan)'
                          : 'var(--bg-tertiary)',
                        width: '36px',
                        height: '36px'
                      }}
                    >
                      <Icon size={18} />
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, marginBottom: '4px' }}>{topic.title}</div>
                      <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                        {topic.description}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Book size={18} style={{ marginRight: '8px', color: 'var(--accent-cyan)' }} />
              {currentTopic?.title || 'Select a Topic'}
            </h3>
          </div>
          <div style={{ color: 'var(--text-secondary)', lineHeight: 1.7, fontSize: '14px' }}>
            {currentTopic ? (
              <div
                style={{ whiteSpace: 'pre-wrap' }}
                dangerouslySetInnerHTML={{
                  __html: currentTopic.content
                    .replace(/^## (.+)$/gm, '<h2 style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin: 20px 0 10px 0;">$1</h2>')
                    .replace(/^### (.+)$/gm, '<h3 style="font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 16px 0 8px 0;">$1</h3>')
                    .replace(/\*\*(.+?)\*\*/g, '<strong style="color: var(--text-primary);">$1</strong>')
                    .replace(/^- (.+)$/gm, '<li style="margin-left: 16px;">$1</li>')
                    .replace(/^(\d+)\. (.+)$/gm, '<li style="margin-left: 16px;"><strong>$1.</strong> $2</li>')
                }}
              />
            ) : (
              <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
                <Book size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
                <p>Select a topic from the left to learn more</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}