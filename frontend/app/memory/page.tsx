'use client';

import { useEffect, useState } from 'react';
import {
  Search,
  Brain,
  Sparkles,
  RefreshCw,
  Clock,
  Star,
  Tag as TagIcon,
  Database,
  Calendar,
  ChevronDown,
  ChevronRight,
  Target,
  Award,
  BookOpen
} from 'lucide-react';
import api from '@/lib/api';

interface Memory {
  id: string;
  content: string;
  importance: number;
  tags: string[];
  timestamp: string;
  access_count: number;
}

interface TimelineGroup {
  year: number;
  month?: number;
  events: Memory[];
}

interface MemoryStats {
  total: number;
  avg_importance: number;
  avg_access_count: number;
  top_tags: [string, number][];
  vector_db: {
    total: number;
    provider: string;
    health: { status: string };
  };
}

const CATEGORY_COLORS: Record<string, string> = {
  learning: 'var(--accent-cyan)',
  project: 'var(--accent-pink)',
  achievement: 'var(--success)',
  goal: 'var(--warning)',
  default: 'var(--primary)'
};

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export default function MemoryPage() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [timelineGroups, setTimelineGroups] = useState<TimelineGroup[]>([]);
  const [stats, setStats] = useState<MemoryStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [semanticQuery, setSemanticQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Memory[]>([]);
  const [searching, setSearching] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'timeline' | 'list'>('timeline');
  const [expandedGroups, setExpandedGroups] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [memoriesData, statsData, timelineData] = await Promise.all([
        api.getMemories(100),
        api.getMemoryStats(),
        api.getTimelineByMonth()
      ]);

      setMemories(memoriesData.memories || []);
      setStats(statsData);
      setTimelineGroups(timelineData.groups || []);
      
      // 默认展开最近的两个分组
      if (timelineData.groups && timelineData.groups.length > 0) {
        const recentGroups = timelineData.groups.slice(0, 2).map((g: TimelineGroup) => 
          g.month ? `${g.year}-${g.month}` : `${g.year}`
        );
        setExpandedGroups(new Set(recentGroups));
      }
    } catch (err) {
      console.error('Failed to load memories:', err);
      setError('Failed to load memories');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    try {
      setSearching(true);
      const results = await api.searchMemories(searchQuery, 20);
      setSearchResults(results.memories || []);
      setViewMode('list');
    } catch (err) {
      console.error('Search failed:', err);
    } finally {
      setSearching(false);
    }
  };

  const handleSemanticSearch = async () => {
    if (!semanticQuery.trim()) return;

    try {
      setSearching(true);
      const results = await api.getSemanticSearch(semanticQuery, 20);
      setSearchResults(results.results || []);
      setViewMode('list');
    } catch (err) {
      console.error('Semantic search failed:', err);
      setError('Semantic search failed. Make sure Vector DB is initialized.');
    } finally {
      setSearching(false);
    }
  };

  const handleSyncToVectorDB = async () => {
    try {
      setSyncing(true);
      await api.syncToVectorDB();
      alert('Synced to Vector DB successfully!');
    } catch (err) {
      console.error('Sync failed:', err);
      alert('Sync failed. Please try again.');
    } finally {
      setSyncing(false);
    }
  };

  const toggleGroup = (groupKey: string) => {
    const newExpanded = new Set(expandedGroups);
    if (newExpanded.has(groupKey)) {
      newExpanded.delete(groupKey);
    } else {
      newExpanded.add(groupKey);
    }
    setExpandedGroups(newExpanded);
  };

  const getCategoryFromTags = (tags: string[]): string => {
    if (tags.includes('learning') || tags.includes('study')) return 'learning';
    if (tags.includes('project') || tags.includes('work')) return 'project';
    if (tags.includes('achievement') || tags.includes('milestone')) return 'achievement';
    if (tags.includes('goal')) return 'goal';
    return 'default';
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'learning': return <BookOpen size={14} />;
      case 'project': return <Target size={14} />;
      case 'achievement': return <Award size={14} />;
      case 'goal': return <Target size={14} />;
      default: return <Brain size={14} />;
    }
  };

  const displayMemories = searchQuery || semanticQuery ? searchResults : memories;

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
        <h1>Memory Timeline</h1>
        <p>Your life events organized chronologically. Powered by semantic search.</p>
      </div>

      <div className="grid grid-4" style={{ marginBottom: '24px' }}>
        <div className="card">
          <div className="card-header">
            <div className="card-icon"><Brain /></div>
          </div>
          <div className="stat-value">{stats?.total || 0}</div>
          <div className="stat-label">Total Memories</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--gradient-pink-purple)' }}>
              <Star />
            </div>
          </div>
          <div className="stat-value">{(stats?.avg_importance || 0).toFixed(2)}</div>
          <div className="stat-label">Avg Importance</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)' }}>
              <Database />
            </div>
          </div>
          <div className="stat-value">{stats?.vector_db?.total || 0}</div>
          <div className="stat-label">Vector DB Items</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)' }}>
              <Calendar />
            </div>
          </div>
          <div className="stat-value">{timelineGroups.length}</div>
          <div className="stat-label">Timeline Groups</div>
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Sparkles size={18} style={{ marginRight: '8px', color: 'var(--accent-cyan)' }} />
            Semantic Search (Vector DB)
          </h3>
          <button
            className="btn btn-secondary"
            onClick={handleSyncToVectorDB}
            disabled={syncing}
          >
            <RefreshCw size={16} className={syncing ? 'spinner' : ''} />
            {syncing ? 'Syncing...' : 'Sync to Vector DB'}
          </button>
        </div>
        <div style={{ display: 'flex', gap: '12px', marginBottom: '16px' }}>
          <input
            type="text"
            className="input"
            placeholder="Search memories with natural language... (e.g., 'What did I learn about Python?')"
            value={semanticQuery}
            onChange={(e) => setSemanticQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSemanticSearch()}
          />
          <button
            className="btn btn-primary"
            onClick={handleSemanticSearch}
            disabled={searching || !semanticQuery.trim()}
          >
            <Search size={16} />
            Search
          </button>
        </div>
        <div
          style={{
            fontSize: '12px',
            color: 'var(--text-muted)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          <div
            style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: stats?.vector_db?.health?.status === 'healthy'
                ? 'var(--success)'
                : 'var(--warning)'
            }}
          />
          Vector DB Status: {stats?.vector_db?.provider || 'in_memory'} (
          {stats?.vector_db?.health?.status || 'unknown'})
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">Quick Search</h3>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              className={`btn ${viewMode === 'timeline' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setViewMode('timeline')}
            >
              <Calendar size={16} />
              Timeline
            </button>
            <button
              className={`btn ${viewMode === 'list' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setViewMode('list')}
            >
              <Brain size={16} />
              List
            </button>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <input
            type="text"
            className="input"
            placeholder="Search by keywords..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button
            className="btn btn-secondary"
            onClick={handleSearch}
            disabled={searching || !searchQuery.trim()}
          >
            <Search size={16} />
            Search
          </button>
          {(searchQuery || semanticQuery) && (
            <button
              className="btn btn-secondary"
              onClick={() => {
                setSearchQuery('');
                setSemanticQuery('');
                setSearchResults([]);
                setViewMode('timeline');
              }}
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {error && <div className="error-message" style={{ marginBottom: '16px' }}>{error}</div>}

      {/* Timeline View */}
      {viewMode === 'timeline' && !searchQuery && !semanticQuery && (
        <div className="timeline-container">
          {timelineGroups.length === 0 ? (
            <div className="card">
              <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px' }}>
                No memories found. Start chatting to create memories!
              </p>
            </div>
          ) : (
            timelineGroups.map((group) => {
              const groupKey = group.month ? `${group.year}-${group.month}` : `${group.year}`;
              const isExpanded = expandedGroups.has(groupKey);
              const category = group.month ? 'month' : 'year';
              
              return (
                <div key={groupKey} className="timeline-group">
                  <div 
                    className="timeline-group-header"
                    onClick={() => toggleGroup(groupKey)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      padding: '12px 16px',
                      background: 'var(--card-bg)',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      marginBottom: isExpanded ? '8px' : '16px',
                      border: '1px solid var(--border)'
                    }}
                  >
                    {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                    <Calendar size={18} style={{ color: 'var(--accent-cyan)' }} />
                    <span style={{ fontWeight: 600, fontSize: '16px' }}>
                      {group.month ? `${MONTHS[group.month - 1]} ${group.year}` : group.year}
                    </span>
                    <span style={{ 
                      color: 'var(--text-muted)', 
                      fontSize: '14px',
                      marginLeft: 'auto' 
                    }}>
                      {group.events.length} events
                    </span>
                  </div>
                  
                  {isExpanded && (
                    <div className="timeline" style={{ marginLeft: '24px' }}>
                      {group.events.map((memory) => {
                        const categoryType = getCategoryFromTags(memory.tags);
                        const categoryColor = CATEGORY_COLORS[categoryType];
                        
                        return (
                          <div key={memory.id} className="timeline-item">
                            <div 
                              className="timeline-dot"
                              style={{ background: categoryColor }}
                            />
                            <div className="timeline-content">
                              <div style={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                gap: '8px',
                                marginBottom: '4px'
                              }}>
                                <span style={{ 
                                  color: categoryColor,
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '4px'
                                }}>
                                  {getCategoryIcon(categoryType)}
                                </span>
                                <span style={{
                                  fontSize: '12px',
                                  color: categoryColor,
                                  fontWeight: 500,
                                  textTransform: 'capitalize'
                                }}>
                                  {categoryType}
                                </span>
                              </div>
                              <div className="timeline-title">{memory.content}</div>
                              <div className="timeline-meta">
                                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                  <Clock size={12} />
                                  {new Date(memory.timestamp).toLocaleString()}
                                </span>
                                <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                                  <Star size={12} />
                                  {memory.importance.toFixed(2)}
                                </span>
                              </div>
                              {memory.tags && memory.tags.length > 0 && (
                                <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                                  {memory.tags.map((tag, idx) => (
                                    <span key={idx} className="tag">{tag}</span>
                                  ))}
                                </div>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>
      )}

      {/* List View */}
      {(viewMode === 'list' || searchQuery || semanticQuery) && (
        <>
          <div className="page-header" style={{ marginTop: '24px' }}>
            <h3>
              {(searchQuery || semanticQuery)
                ? `Search Results (${searchResults.length})`
                : 'Recent Memories'}
            </h3>
          </div>

          <div className="timeline">
            {displayMemories.length === 0 ? (
              <div className="card">
                <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px' }}>
                  No memories found. Start chatting to create memories!
                </p>
              </div>
            ) : (
              displayMemories.map((memory) => {
                const categoryType = getCategoryFromTags(memory.tags);
                const categoryColor = CATEGORY_COLORS[categoryType];
                
                return (
                  <div key={memory.id} className="timeline-item">
                    <div 
                      className="timeline-dot"
                      style={{ background: categoryColor }}
                    />
                    <div className="timeline-content">
                      <div style={{ 
                        display: 'flex', 
                        alignItems: 'center', 
                        gap: '8px',
                        marginBottom: '4px'
                      }}>
                        <span style={{ 
                          color: categoryColor,
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px'
                        }}>
                          {getCategoryIcon(categoryType)}
                        </span>
                        <span style={{
                          fontSize: '12px',
                          color: categoryColor,
                          fontWeight: 500,
                          textTransform: 'capitalize'
                        }}>
                          {categoryType}
                        </span>
                      </div>
                      <div className="timeline-title">{memory.content}</div>
                      <div className="timeline-meta">
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Clock size={12} />
                          {new Date(memory.timestamp).toLocaleString()}
                        </span>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <Star size={12} />
                          {memory.importance.toFixed(2)}
                        </span>
                      </div>
                      {memory.tags && memory.tags.length > 0 && (
                        <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                          {memory.tags.map((tag, idx) => (
                            <span key={idx} className="tag">{tag}</span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </>
      )}
    </div>
  );
}
