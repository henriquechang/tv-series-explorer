import type { ShowSearchResult, ShowWithEpisodes } from '../types';

const API_BASE = '/api';

class ApiError extends Error {
  constructor(_status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new ApiError(response.status, `HTTP ${response.status}`);
  }
  return response.json();
}

export const api = {
  async searchShows(query: string): Promise<ShowSearchResult[]> {
    const encoded = encodeURIComponent(query);
    return fetchJson<ShowSearchResult[]>(`${API_BASE}/shows/search?q=${encoded}`);
  },

  async getShowDetails(id: number): Promise<ShowWithEpisodes> {
    return fetchJson<ShowWithEpisodes>(`${API_BASE}/shows/${id}/details`);
  }
};