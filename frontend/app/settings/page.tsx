'use client';

import { useState } from 'react';
import { Settings, Database, Sparkles, User, Bell, Shield } from 'lucide-react';

interface SystemConfig {
  vectorDB: {
    provider: string;
    status: string;
  };
  neo4j: {
    uri: string;
    status: string;
  };
  llm: {
    model: string;
    status: string;
  };
}

export default function SettingsPage() {
  const [config, setConfig] = useState<SystemConfig>({
    vectorDB: {
      provider: 'in_memory',
      status: 'healthy'
    },
    neo4j: {
      uri: 'bolt://localhost:7687',
      status: 'disconnected'
    },
    llm: {
      model: 'simulated',
      status: 'ready'
    }
  });

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Settings</h1>
        <p>Configure your TitanOS system settings and integrations.</p>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Database size={18} style={{ marginRight: '8px', color: 'var(--accent-cyan)' }} />
            Vector Database
          </h3>
        </div>
        <div className="grid grid-2" style={{ marginTop: '16px' }}>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'block' }}>
              Provider
            </label>
            <select className="input">
              <option value="in_memory">In-Memory</option>
              <option value="qdrant">Qdrant</option>
              <option value="weaviate">Weaviate</option>
              <option value="pinecone">Pinecone</option>
            </select>
          </div>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'block' }}>
              Status
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px', background: 'var(--bg-tertiary)', borderRadius: '10px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success)' }} />
              <span>{config.vectorDB.status}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Sparkles size={18} style={{ marginRight: '8px', color: 'var(--accent-purple)' }} />
            Neo4j Graph Database
          </h3>
        </div>
        <div className="grid grid-2" style={{ marginTop: '16px' }}>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'block' }}>
              Connection URI
            </label>
            <input
              type="text"
              className="input"
              placeholder="bolt://localhost:7687"
              defaultValue={config.neo4j.uri}
            />
          </div>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'block' }}>
              Status
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px', background: 'var(--bg-tertiary)', borderRadius: '10px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: config.neo4j.status === 'connected' ? 'var(--success)' : 'var(--warning)' }} />
              <span>{config.neo4j.status}</span>
            </div>
          </div>
        </div>
        <div style={{ marginTop: '16px', display: 'flex', gap: '12px' }}>
          <button className="btn btn-primary">Connect</button>
          <button className="btn btn-secondary">Test Connection</button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Settings size={18} style={{ marginRight: '8px', color: 'var(--accent-pink)' }} />
            LLM Model
          </h3>
        </div>
        <div className="grid grid-2" style={{ marginTop: '16px' }}>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'block' }}>
              Model Type
            </label>
            <select className="input">
              <option value="simulated">Simulated (Testing)</option>
              <option value="openai">OpenAI GPT</option>
              <option value="anthropic">Anthropic Claude</option>
              <option value="local">Local Model</option>
            </select>
          </div>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '8px', display: 'block' }}>
              Status
            </label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px', background: 'var(--bg-tertiary)', borderRadius: '10px' }}>
              <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success)' }} />
              <span>{config.llm.status}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">System Information</h3>
        </div>
        <div className="grid grid-2">
          <div style={{ padding: '16px', background: 'var(--bg-tertiary)', borderRadius: '12px' }}>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '8px' }}>Version</div>
            <div style={{ fontSize: '18px', fontWeight: 600, color: 'var(--accent-purple)' }}>v2.0.0</div>
          </div>
          <div style={{ padding: '16px', background: 'var(--bg-tertiary)', borderRadius: '12px' }}>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '8px' }}>Framework</div>
            <div style={{ fontSize: '18px', fontWeight: 600, color: 'var(--accent-cyan)' }}>Next.js + React</div>
          </div>
        </div>
      </div>
    </div>
  );
}