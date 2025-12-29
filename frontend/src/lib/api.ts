const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DailyLog {
  id: string;
  user_id: string;
  log_date: string;
  raw_text: string;
  structured_data?: any;
  mood?: string;
  difficulty_level?: string;
  created_at: string;
  updated_at: string;
}

export interface SummaryRequest {
  mode: 'daily' | 'weekly' | 'monthly';
  start_date: string;
  end_date?: string;
}

export class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Daily Logs
  async createDailyLog(log_date: string, raw_text: string): Promise<DailyLog> {
    const response = await fetch(`${this.baseUrl}/api/v1/logs/daily`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ log_date, raw_text }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create daily log');
    }

    return response.json();
  }

  async getDailyLog(date: string): Promise<DailyLog> {
    const response = await fetch(`${this.baseUrl}/api/v1/logs/daily/${date}`);
    
    if (!response.ok) {
      throw new Error('Log not found');
    }

    return response.json();
  }

  async listDailyLogs(skip: number = 0, limit: number = 10): Promise<DailyLog[]> {
    const response = await fetch(
      `${this.baseUrl}/api/v1/logs/daily?skip=${skip}&limit=${limit}`
    );

    if (!response.ok) {
      throw new Error('Failed to fetch logs');
    }

    return response.json();
  }

  // Reasoning
  async generateSummary(request: SummaryRequest): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/reasoning/summarize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to generate summary');
    }

    return response.json();
  }

  async explainConcept(concept_name: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/reasoning/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ concept_name }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to explain concept');
    }

    return response.json();
  }

  async semanticSearch(query: string, searchType: 'concepts' | 'logs' = 'concepts', limit: number = 5): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/reasoning/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, search_type: searchType, limit }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Search failed');
    }

    return response.json();
  }

  async getLearningGuidance(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/v1/reasoning/guidance`);

    if (!response.ok) {
      throw new Error('Failed to get guidance');
    }

    return response.json();
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/health`);
    return response.json();
  }
}

export const api = new ApiClient();
