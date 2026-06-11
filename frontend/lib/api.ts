const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8888';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: any;
  headers?: Record<string, string>;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { method = 'GET', body, headers = {} } = options;

    const config: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
    };

    if (body) {
      config.body = JSON.stringify(body);
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, config);

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Chat APIs
  async sendChat(message: string) {
    return this.request<any>('/chat', {
      method: 'POST',
      body: { message },
    });
  }

  async getChatHistory(limit: number = 50) {
    return this.request<any>(`/chat/history?limit=${limit}`);
  }

  async getChatStats() {
    return this.request<any>('/chat/stats');
  }

  // Memory APIs
  async getMemories(limit: number = 20) {
    return this.request<any>(`/memory?limit=${limit}`);
  }

  async getMemoryStats() {
    return this.request<any>('/memory/stats');
  }

  async searchMemories(query: string, limit: number = 10) {
    return this.request<any>(`/memory/search/${encodeURIComponent(query)}?limit=${limit}`);
  }

  async getSemanticSearch(query: string, limit: number = 10) {
    return this.request<any>(`/memory/semantic/${encodeURIComponent(query)}?limit=${limit}`);
  }

  async getImportantMemories(limit: number = 20) {
    return this.request<any>(`/memory/important?limit=${limit}`);
  }

  async syncToVectorDB() {
    return this.request<any>('/memory/sync-vector-db', { method: 'POST' });
  }

  // Knowledge Graph APIs
  async getKnowledgeStats() {
    return this.request<any>('/knowledge/stats');
  }

  async queryKnowledge(entityName?: string, entityType?: string, relationType?: string) {
    const params = new URLSearchParams();
    if (entityName) params.append('entity_name', entityName);
    if (entityType) params.append('entity_type', entityType);
    if (relationType) params.append('relation_type', relationType);
    return this.request<any>(`/knowledge/query?${params.toString()}`);
  }

  async analyzeText(text: string) {
    return this.request<any>('/knowledge/analyze', {
      method: 'POST',
      body: { text },
    });
  }

  async extractFromText(text: string) {
    return this.request<any>(`/knowledge/extract?text=${encodeURIComponent(text)}`, {
      method: 'POST',
    });
  }

  async createEntity(name: string, entityType: string, description: string = '') {
    return this.request<any>('/knowledge/entity', {
      method: 'POST',
      body: { name, entity_type: entityType, description },
    });
  }

  async searchEntity(name: string) {
    return this.request<any>(`/knowledge/entity/search/${encodeURIComponent(name)}`);
  }

  async getNeighbors(entityId: string, depth: number = 1, relationType?: string) {
    let url = `/knowledge/entity/${entityId}/neighbors?depth=${depth}`;
    if (relationType) url += `&relation_type=${relationType}`;
    return this.request<any>(url);
  }

  async findPath(fromEntity: string, toEntity: string, maxDepth: number = 5) {
    return this.request<any>(`/knowledge/path?from_entity_name=${encodeURIComponent(fromEntity)}&to_entity_name=${encodeURIComponent(toEntity)}&max_depth=${maxDepth}`);
  }

  async exportCypher() {
    return this.request<any>('/knowledge/cypher');
  }

  async executeCypher(query: string) {
    return this.request<any>(`/knowledge/neo4j/cypher?query=${encodeURIComponent(query)}`, {
      method: 'POST',
    });
  }

  // Vector DB APIs
  async getVectorDBStats() {
    return this.request<any>('/vector-db/stats');
  }

  async initVectorDB(provider: string, config: any = {}) {
    return this.request<any>('/vector-db/init', {
      method: 'POST',
      body: { provider, ...config },
    });
  }

  // Dashboard APIs
  async getDashboardMetrics() {
    return this.request<any>('/dashboard/metrics');
  }

  async getDashboardSummary() {
    return this.request<any>('/dashboard/summary');
  }

  async getGrowthScore() {
    return this.request<any>('/dashboard/growth-score');
  }

  // Goal Tree APIs
  async getGoalTree() {
    return this.request<any>('/goal-tree/tree');
  }

  async getGoalSummary() {
    return this.request<any>('/goal-tree/summary');
  }

  // Timeline APIs
  async getTimeline(limit: number = 20) {
    return this.request<any>(`/timeline?limit=${limit}`);
  }

  async getTimelineStats() {
    return this.request<any>('/timeline/stats');
  }

  async getTimelineByYear() {
    return this.request<any>('/timeline');
  }

  async getTimelineByMonth() {
    return this.request<any>('/timeline/monthly');
  }

  async getTimelineEvents() {
    return this.request<any>('/timeline/events');
  }

  async getTimelineSummary() {
    return this.request<any>('/timeline/summary');
  }

  async getMilestones() {
    return this.request<any>('/timeline/milestones');
  }

  // LLM APIs
  async chatWithLLM(message: string, sessionId?: string, systemPrompt?: string) {
    return this.request<any>('/chat/llm', {
      method: 'POST',
      body: { message, session_id: sessionId, system_prompt: systemPrompt },
    });
  }

  async getLLMConfig() {
    return this.request<any>('/llm/config');
  }

  async setLLMConfig(provider: string, apiKey: string, model?: string, baseUrl?: string) {
    return this.request<any>('/llm/config', {
      method: 'POST',
      body: { provider, api_key: apiKey, model, base_url: baseUrl },
    });
  }

  async getLLMStatus() {
    return this.request<any>('/llm/status');
  }

  // Health check
  async healthCheck() {
    return this.request<any>('/health');
  }
}

export const api = new ApiService();
export default api;