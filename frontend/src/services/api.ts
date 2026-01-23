import type { ShowSearchResult, ShowWithEpisodes, Comment } from '../types';

const API_BASE = '/api';

class ApiError extends Error {
  constructor(_status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
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
  },

  async getShowInsight(showId: number): Promise<{ insight: string; source: string }> {
    return fetchJson<{ insight: string; source: string }>(`${API_BASE}/shows/${showId}/insight`);
  },

  async getEpisodeInsight(showId: number, episodeId: number): Promise<{ insight: string; source: string }> {
    return fetchJson<{ insight: string; source: string }>(
      `${API_BASE}/shows/${showId}/episodes/${episodeId}/insight`
    );
  },

  async getShowComments(showId: number): Promise<Comment[]> {
    return fetchJson<Comment[]>(`${API_BASE}/shows/${showId}/comments`);
  },

  async addShowComment(showId: number, text: string): Promise<Comment> {
    const response = await fetch(`${API_BASE}/shows/${showId}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!response.ok) {
      throw new ApiError(response.status, `HTTP ${response.status}`);
    }
    return response.json();
  },

  async getEpisodeComments(episodeId: number): Promise<Comment[]> {
    return fetchJson<Comment[]>(`${API_BASE}/episodes/${episodeId}/comments`);
  },

  async addEpisodeComment(showId: number, episodeId: number, text: string): Promise<Comment> {
    const response = await fetch(`${API_BASE}/shows/${showId}/episodes/${episodeId}/comments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!response.ok) {
      throw new ApiError(response.status, `HTTP ${response.status}`);
    }
    return response.json();
  },

  async deleteComment(commentId: number): Promise<void> {
    const response = await fetch(`${API_BASE}/comments/${commentId}`, {
      method: 'DELETE'
    });
    if (!response.ok) {
      throw new ApiError(response.status, `HTTP ${response.status}`);
    }
  },

  async getWatchedEpisodes(showId: number): Promise<{ episode_id: number; watched: boolean }[]> {
    return fetchJson<{ episode_id: number; watched: boolean }[]>(`${API_BASE}/shows/${showId}/watched`);
  },

  async isEpisodeWatched(showId: number, episodeId: number): Promise<{ episode_id: number; watched: boolean }> {
    return fetchJson<{ episode_id: number; watched: boolean }>(`${API_BASE}/shows/${showId}/episodes/${episodeId}/watched`);
  },

  async markEpisodeWatched(showId: number, episodeId: number): Promise<{ status: string; watched: boolean }> {
    const response = await fetch(`${API_BASE}/shows/${showId}/episodes/${episodeId}/watched`, {
      method: 'PUT'
    });
    if (!response.ok) {
      throw new ApiError(response.status, `HTTP ${response.status}`);
    }
    return response.json();
  },

  async unmarkEpisodeWatched(showId: number, episodeId: number): Promise<{ status: string; watched: boolean }> {
    const response = await fetch(`${API_BASE}/shows/${showId}/episodes/${episodeId}/watched`, {
      method: 'DELETE'
    });
    if (!response.ok) {
      throw new ApiError(response.status, `HTTP ${response.status}`);
    }
    return response.json();
  }
};