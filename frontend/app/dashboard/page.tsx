'use client';

import { useEffect, useState } from 'react';
import {
  Brain,
  MessageSquare,
  Target,
  TrendingUp,
  Zap,
  Clock,
  Sparkles
} from 'lucide-react';
import api from '@/lib/api';

interface DashboardData {
  growth_score: number;
  total_memories: number;
  total_chats: number;
  total_goals: number;
  recent_memories: any[];
  recent_activities: any[];
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const [metrics, memoryStats, chatStats] = await Promise.all([
        api.getDashboardMetrics(),
        api.getMemoryStats(),
        api.getChatStats()
      ]);

      setData({
        growth_score: metrics?.growth_score || 0,
        total_memories: memoryStats?.total || 0,
        total_chats: chatStats?.total_messages || 0,
        total_goals: 0,
        recent_memories: memoryStats?.top_tags?.slice(0, 5) || [],
        recent_activities: []
      });
    } catch (err) {
      console.error('Failed to load dashboard:', err);
      setError('Failed to load dashboard data');
      setData({
        growth_score: 0,
        total_memories: 0,
        total_chats: 0,
        total_goals: 0,
        recent_memories: [],
        recent_activities: []
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading">
          <div className="spinner" />
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Welcome back! Here&apos;s your AI assistant overview.</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="grid grid-4" style={{ marginBottom: '32px' }}>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--gradient-purple-cyan)' }}>
              <Brain />
            </div>
          </div>
          <div className="stat-value">{data?.total_memories || 0}</div>
          <div className="stat-label">Total Memories</div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--gradient-pink-purple)' }}>
              <MessageSquare />
            </div>
          </div>
          <div className="stat-value">{data?.total_chats || 0}</div>
          <div className="stat-label">Total Chats</div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)' }}>
              <Target />
            </div>
          </div>
          <div className="stat-value">{data?.total_goals || 0}</div>
          <div className="stat-label">Active Goals</div>
        </div>

        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)' }}>
              <TrendingUp />
            </div>
          </div>
          <div className="stat-value">{data?.growth_score || 0}%</div>
          <div className="stat-label">Growth Score</div>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Memories</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data?.recent_memories.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
                No memories yet. Start chatting to create memories!
              </p>
            ) : (
              data?.recent_memories.map((tag: any, index: number) => (
                <div
                  key={index}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '12px',
                    background: 'var(--bg-tertiary)',
                    borderRadius: '10px'
                  }}
                >
                  <span style={{ fontSize: '14px' }}>{tag[0]}</span>
                  <span className="badge badge-purple">{tag[1]} times</span>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Quick Actions</h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <button
              className="btn btn-primary"
              style={{ justifyContent: 'flex-start' }}
              onClick={() => window.location.href = '/chat'}
            >
              <MessageSquare size={18} />
              Start a new conversation
            </button>
            <button
              className="btn btn-secondary"
              style={{ justifyContent: 'flex-start' }}
              onClick={() => window.location.href = '/memory'}
            >
              <Brain size={18} />
              Explore memories
            </button>
            <button
              className="btn btn-secondary"
              style={{ justifyContent: 'flex-start' }}
              onClick={() => window.location.href = '/knowledge-graph'}
            >
              <Sparkles size={18} />
              View knowledge graph
            </button>
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">System Status</h3>
        </div>
        <div className="grid grid-3">
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                background: 'var(--success)'
              }}
            />
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
              Memory Engine: Active
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                background: 'var(--success)'
              }}
            />
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
              Vector DB: In-Memory
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div
              style={{
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                background: 'var(--success)'
              }}
            />
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
              Knowledge Graph: Ready
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}