export interface ShowSearchResult {
  id: number;
  name: string;
  year: number | null;
  poster_url: string | null;
}

export interface Episode {
  id: number;
  season: number;
  number: number;
  name: string;
  summary: string | null;
  airdate: string | null;
}

export interface Season {
  season_number: number;
  episodes: Episode[];
}

export interface ShowWithEpisodes {
  id: number;
  name: string;
  year: number | null;
  poster_url: string | null;
  summary: string | null;
  genres: string[];
  seasons: Season[];
}

export interface Comment {
  id: number;
  show_id: number;
  episode_id: number | null;
  text: string;
  created_at: string;
}

export interface WatchedEpisode {
  episode_id: number;
  watched_at: string;
}