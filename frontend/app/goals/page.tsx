'use client';

import { useEffect, useState } from 'react';
import { Target, Plus, CheckCircle, Clock, TrendingUp, AlertCircle } from 'lucide-react';
import api from '@/lib/api';

interface Goal {
  id: string;
  title: string;
  description: string;
  status: string;
  priority: string;
  progress: number;
  created_at: string;
  deadline?: string;
}

interface GoalTree {
  goals: Goal[];
  total: number;
  completed: number;
  in_progress: number;
  overdue: number;
}

export default function GoalsPage() {
  const [goalTree, setGoalTree] = useState<GoalTree | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadGoals();
  }, []);

  const loadGoals = async () => {
    try {
      setLoading(true);
      const data = await api.getGoalTree();
      setGoalTree(data);
    } catch (err) {
      console.error('Failed to load goals:', err);
      setError('Failed to load goals. Please check if the backend is running.');
      setGoalTree({
        goals: [],
        total: 0,
        completed: 0,
        in_progress: 0,
        overdue: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'var(--success)';
      case 'in_progress':
        return 'var(--accent-cyan)';
      case 'overdue':
        return 'var(--error)';
      default:
        return 'var(--text-muted)';
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'badge-purple';
      case 'medium':
        return 'badge-cyan';
      case 'low':
        return 'badge-pink';
      default:
        return 'badge-purple';
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
        <h1>Goal Tree</h1>
        <p>Track and manage your goals with visual progress monitoring.</p>
      </div>

      <div className="grid grid-4" style={{ marginBottom: '24px' }}>
        <div className="card">
          <div className="card-header">
            <div className="card-icon"><Target /></div>
          </div>
          <div className="stat-value">{goalTree?.total || 0}</div>
          <div className="stat-label">Total Goals</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--success)' }}>
              <CheckCircle />
            </div>
          </div>
          <div className="stat-value">{goalTree?.completed || 0}</div>
          <div className="stat-label">Completed</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--accent-cyan)' }}>
              <TrendingUp />
            </div>
          </div>
          <div className="stat-value">{goalTree?.in_progress || 0}</div>
          <div className="stat-label">In Progress</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--error)' }}>
              <AlertCircle />
            </div>
          </div>
          <div className="stat-value">{goalTree?.overdue || 0}</div>
          <div className="stat-label">Overdue</div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">Your Goal Tree</h3>
          <button className="btn btn-primary">
            <Plus size={16} />
            Add New Goal
          </button>
        </div>

        {error && <div className="error-message" style={{ marginBottom: '16px' }}>{error}</div>}

        <div className="timeline">
          {goalTree?.goals?.length === 0 ? (
            <div
              style={{
                textAlign: 'center',
                padding: '60px 20px',
                color: 'var(--text-muted)'
              }}
            >
              <Target size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
              <p style={{ fontSize: '16px', marginBottom: '8px' }}>
                No goals yet
              </p>
              <p style={{ fontSize: '13px' }}>
                Create your first goal to start tracking your progress
              </p>
            </div>
          ) : (
            goalTree?.goals?.map((goal) => (
              <div key={goal.id} className="timeline-item">
                <div
                  style={{
                    width: '12px',
                    height: '12px',
                    borderRadius: '50%',
                    background: getStatusColor(goal.status),
                    marginTop: '4px',
                    flexShrink: 0
                  }}
                />
                <div className="timeline-content" style={{ flex: 1 }}>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      marginBottom: '8px'
                    }}
                  >
                    <div className="timeline-title">{goal.title}</div>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                      <span className={`badge ${getPriorityBadge(goal.priority)}`}>
                        {goal.priority}
                      </span>
                      <span className="badge badge-cyan">{goal.status}</span>
                    </div>
                  </div>
                  <div className="timeline-description">{goal.description}</div>
                  <div style={{ marginTop: '12px' }}>
                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        fontSize: '12px',
                        color: 'var(--text-muted)',
                        marginBottom: '6px'
                      }}
                    >
                      <span>Progress</span>
                      <span>{goal.progress}%</span>
                    </div>
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{
                          width: `${goal.progress}%`,
                          background: getStatusColor(goal.status)
                        }}
                      />
                    </div>
                  </div>
                  <div className="timeline-meta" style={{ marginTop: '12px' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Clock size={12} />
                      Created: {new Date(goal.created_at).toLocaleDateString()}
                    </span>
                    {goal.deadline && (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <AlertCircle size={12} />
                        Deadline: {new Date(goal.deadline).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Goal Categories</h3>
        </div>
        <div className="grid grid-3">
          <div
            style={{
              padding: '20px',
              background: 'var(--bg-tertiary)',
              borderRadius: '12px',
              textAlign: 'center'
            }}
          >
            <div
              style={{
                fontSize: '28px',
                fontWeight: 700,
                color: 'var(--accent-purple)',
                marginBottom: '8px'
              }}
            >
              Career
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              Professional development goals
            </div>
          </div>
          <div
            style={{
              padding: '20px',
              background: 'var(--bg-tertiary)',
              borderRadius: '12px',
              textAlign: 'center'
            }}
          >
            <div
              style={{
                fontSize: '28px',
                fontWeight: 700,
                color: 'var(--accent-cyan)',
                marginBottom: '8px'
              }}
            >
              Learning
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              Education and skill acquisition
            </div>
          </div>
          <div
            style={{
              padding: '20px',
              background: 'var(--bg-tertiary)',
              borderRadius: '12px',
              textAlign: 'center'
            }}
          >
            <div
              style={{
                fontSize: '28px',
                fontWeight: 700,
                color: 'var(--accent-pink)',
                marginBottom: '8px'
              }}
            >
              Personal
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
              Life and wellness goals
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}