'use client';

import { useEffect, useState, useRef } from 'react';
import {
  GitBranch,
  Search,
  Plus,
  RefreshCw,
  Play,
  Eye,
  Sparkles,
  Database,
  Link2
} from 'lucide-react';
import api from '@/lib/api';

interface Entity {
  id: string;
  name: string;
  type: string;
  description: string;
}

interface Relation {
  id: string;
  from: string;
  to: string;
  type: string;
  weight: number;
}

interface GraphStats {
  total_entities: number;
  total_relations: number;
  entity_types: Record<string, number>;
  relation_types: Record<string, number>;
  use_neo4j: boolean;
  neo4j_connected: boolean;
}

export default function KnowledgeGraphPage() {
  const [stats, setStats] = useState<GraphStats | null>(null);
  const [entities, setEntities] = useState<Entity[]>([]);
  const [relations, setRelations] = useState<Relation[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchName, setSearchName] = useState('');
  const [analyzeText, setAnalyzeText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [pathFrom, setPathFrom] = useState('');
  const [pathTo, setPathTo] = useState('');
  const [pathResult, setPathResult] = useState<any>(null);
  const graphRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const statsData = await api.getKnowledgeStats();
      setStats(statsData);

      if (statsData.total_entities > 0) {
        const queryResult = await api.queryKnowledge();
        setEntities(queryResult.entities || []);
        setRelations(queryResult.relations || []);
      }
    } catch (err) {
      console.error('Failed to load knowledge graph:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchName.trim()) return;

    try {
      const result = await api.searchEntity(searchName);
      if (result.entity) {
        setEntities([result.entity]);
        const neighbors = await api.getNeighbors(result.entity.id, 2);
        if (neighbors.neighbors) {
          const neighborEntities = neighbors.neighbors.map((n: any) => n[0]);
          const neighborRelations = neighbors.neighbors.map((n: any) => n[1]);
          setEntities(prev => [...prev, ...neighborEntities]);
          setRelations(prev => [...prev, ...neighborRelations]);
        }
      }
    } catch (err) {
      console.error('Search failed:', err);
    }
  };

  const handleAnalyze = async () => {
    if (!analyzeText.trim()) return;

    try {
      setAnalyzing(true);
      const result = await api.analyzeText(analyzeText);
      setAnalysisResult(result);
      await loadData();
    } catch (err) {
      console.error('Analysis failed:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleFindPath = async () => {
    if (!pathFrom.trim() || !pathTo.trim()) return;

    try {
      const result = await api.findPath(pathFrom, pathTo, 5);
      setPathResult(result);
    } catch (err) {
      console.error('Path finding failed:', err);
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
        <h1>Knowledge Graph</h1>
        <p>Visualize and explore entity relationships powered by Neo4j and LLM.</p>
      </div>

      <div className="grid grid-4" style={{ marginBottom: '24px' }}>
        <div className="card">
          <div className="card-header">
            <div className="card-icon"><GitBranch /></div>
          </div>
          <div className="stat-value">{stats?.total_entities || 0}</div>
          <div className="stat-label">Total Entities</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'var(--gradient-pink-purple)' }}>
              <Link2 />
            </div>
          </div>
          <div className="stat-value">{stats?.total_relations || 0}</div>
          <div className="stat-label">Total Relations</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)' }}>
              <Database />
            </div>
          </div>
          <div className="stat-value">{stats?.use_neo4j ? 'Neo4j' : 'Local'}</div>
          <div className="stat-label">Storage</div>
        </div>
        <div className="card">
          <div className="card-header">
            <div className="card-icon" style={{ background: stats?.neo4j_connected ? 'var(--success)' : 'var(--warning)' }}>
              <Sparkles />
            </div>
          </div>
          <div className="stat-value">{stats?.neo4j_connected ? 'Online' : 'Offline'}</div>
          <div className="stat-label">Neo4j Status</div>
        </div>
      </div>

      <div className="grid grid-2" style={{ marginBottom: '24px' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Sparkles size={18} style={{ marginRight: '8px', color: 'var(--accent-cyan)' }} />
              LLM Text Analysis
            </h3>
          </div>
          <textarea
            className="input"
            placeholder="Enter text to extract entities and relationships... (e.g., '机器学习属于人工智能，深度学习是机器学习的一种')"
            value={analyzeText}
            onChange={(e) => setAnalyzeText(e.target.value)}
            rows={4}
            style={{ marginBottom: '12px', resize: 'vertical' }}
          />
          <button
            className="btn btn-primary"
            onClick={handleAnalyze}
            disabled={analyzing || !analyzeText.trim()}
          >
            {analyzing ? (
              <>
                <div className="spinner" style={{ width: '16px', height: '16px' }} />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles size={16} />
                Analyze with LLM
              </>
            )}
          </button>
          {analysisResult && (
            <div style={{ marginTop: '16px' }}>
              <div className="success-message">
                <p><strong>Summary:</strong> {analysisResult.summary}</p>
                <p style={{ marginTop: '8px' }}>
                  Found {analysisResult.entities_found} entities and{' '}
                  {analysisResult.relations_found} relations
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Search size={18} style={{ marginRight: '8px', color: 'var(--accent-purple)' }} />
              Find Path Between Entities
            </h3>
          </div>
          <div style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
            <input
              type="text"
              className="input"
              placeholder="From entity..."
              value={pathFrom}
              onChange={(e) => setPathFrom(e.target.value)}
            />
            <input
              type="text"
              className="input"
              placeholder="To entity..."
              value={pathTo}
              onChange={(e) => setPathTo(e.target.value)}
            />
          </div>
          <button
            className="btn btn-secondary"
            onClick={handleFindPath}
            disabled={!pathFrom.trim() || !pathTo.trim()}
          >
            <Play size={16} />
            Find Path
          </button>
          {pathResult && (
            <div style={{ marginTop: '16px' }}>
              {pathResult.paths_found > 0 ? (
                <div className="success-message">
                  <p>Found {pathResult.paths_found} path(s)!</p>
                </div>
              ) : (
                <div className="error-message">
                  <p>No path found between entities.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">Search Entities</h3>
          <div style={{ display: 'flex', gap: '12px' }}>
            <input
              type="text"
              className="input"
              placeholder="Search by entity name..."
              value={searchName}
              onChange={(e) => setSearchName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              style={{ width: '300px' }}
            />
            <button className="btn btn-secondary" onClick={handleSearch}>
              <Search size={16} />
              Search
            </button>
            <button className="btn btn-secondary" onClick={loadData}>
              <RefreshCw size={16} />
              Refresh
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Entities</h3>
          </div>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {entities.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>
                No entities yet. Use LLM Text Analysis to extract entities from text.
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {entities.map((entity) => (
                  <div
                    key={entity.id}
                    style={{
                      padding: '12px',
                      background: 'var(--bg-tertiary)',
                      borderRadius: '10px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 500 }}>{entity.name}</div>
                      <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                        {entity.description?.slice(0, 50) || 'No description'}
                      </div>
                    </div>
                    <span className="badge badge-purple">{entity.type}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Relations</h3>
          </div>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {relations.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '20px' }}>
                No relations yet. Create entities and connect them.
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {relations.map((relation) => (
                  <div
                    key={relation.id}
                    style={{
                      padding: '12px',
                      background: 'var(--bg-tertiary)',
                      borderRadius: '10px',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px'
                    }}
                  >
                    <span style={{ fontWeight: 500 }}>{relation.from}</span>
                    <span className="badge badge-cyan">{relation.type}</span>
                    <span style={{ fontWeight: 500 }}>{relation.to}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '24px' }}>
        <div className="card-header">
          <h3 className="card-title">
            <Eye size={18} style={{ marginRight: '8px', color: 'var(--accent-cyan)' }} />
            Graph Visualization
          </h3>
        </div>
        <div
          ref={graphRef}
          className="graph-container"
          style={{ height: '500px', position: 'relative' }}
        >
          {entities.length === 0 ? (
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
              <GitBranch size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
              <p>No graph data to display</p>
              <p style={{ fontSize: '13px', marginTop: '8px' }}>
                Extract entities from text to build your knowledge graph
              </p>
            </div>
          ) : (
            <div style={{ position: 'relative', width: '100%', height: '100%' }}>
              {entities.map((entity, index) => {
                const angle = (index / entities.length) * 2 * Math.PI;
                const radius = 150;
                const centerX = 250;
                const centerY = 250;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);

                return (
                  <div
                    key={entity.id}
                    className="graph-node"
                    style={{
                      left: `${x}px`,
                      top: `${y}px`,
                      transform: 'translate(-50%, -50%)',
                      background: entity.type === 'person'
                        ? 'var(--gradient-pink-purple)'
                        : entity.type === 'technology'
                          ? 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)'
                          : 'var(--gradient-purple-cyan)'
                    }}
                  >
                    {entity.name}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}