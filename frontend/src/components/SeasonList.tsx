import { useState, useEffect } from 'react';
import type { Season } from '../types';
import { AIInsight } from './AIInsight';
import { Comments } from './Comments';
import { api } from '../services/api';

export function SeasonList({ seasons, showId }: { seasons: Season[]; showId: number }) {
  const [expandedSeason, setExpandedSeason] = useState<number | null>(1);
  const [expandedEpisode, setExpandedEpisode] = useState<number | null>(null);
  const [watchedEpisodes, setWatchedEpisodes] = useState<Set<number>>(new Set());

  useEffect(() => {
    const loadWatchedEpisodes = async () => {
      try {
        const watched = await api.getWatchedEpisodes(showId);
        setWatchedEpisodes(new Set(watched.map(ep => ep.episode_id)));
      } catch (error) {
        console.error('Failed to load watched episodes:', error);
      }
    };
    loadWatchedEpisodes();
  }, [showId]);

  const toggleWatched = async (episodeId: number) => {
    const isWatched = watchedEpisodes.has(episodeId);
    
    if (isWatched) {
      setWatchedEpisodes(prev => {
        const next = new Set(prev);
        next.delete(episodeId);
        return next;
      });
    } else {
      setWatchedEpisodes(prev => new Set(prev).add(episodeId));
    }
    
    try {
      if (isWatched) {
        await api.unmarkEpisodeWatched(showId, episodeId);
      } else {
        await api.markEpisodeWatched(showId, episodeId);
      }
    } catch (error) {
      if (isWatched) {
        setWatchedEpisodes(prev => new Set(prev).add(episodeId));
      } else {
        setWatchedEpisodes(prev => {
          const next = new Set(prev);
          next.delete(episodeId);
          return next;
        });
      }
    }
  };

  return (
    <div className="season-list">
      {seasons.map(season => (
        <div key={season.season_number} className="season">
          <button
            className="season-header"
            onClick={() => setExpandedSeason(expandedSeason === season.season_number ? null : season.season_number)}
          >
            <span>Season {season.season_number}</span>
            <span className="episode-count">{season.episodes.length} episodes</span>
            <span className="expand-icon">{expandedSeason === season.season_number ? '−' : '+'}</span>
          </button>
          
          {expandedSeason === season.season_number && (
            <ul className="episode-list">
              {season.episodes.map(ep => (
                <li key={ep.id} className={`episode-item ${watchedEpisodes.has(ep.id) ? 'watched' : ''}`}>
                  <div className="episode-header">
                    <input
                      type="checkbox"
                      checked={watchedEpisodes.has(ep.id)}
                      onChange={() => toggleWatched(ep.id)}
                      className="watched-checkbox"
                      onClick={(e) => e.stopPropagation()}
                    />
                    <div 
                      onClick={() => setExpandedEpisode(expandedEpisode === ep.id ? null : ep.id)}
                      style={{ cursor: 'pointer', flex: 1 }}
                    >
                      <span className="episode-number">{ep.number}</span>
                      <span className="episode-name">{ep.name}</span>
                      {ep.airdate && <span className="episode-airdate">{ep.airdate}</span>}
                    </div>
                  </div>
                  {expandedEpisode === ep.id && (
                    <>
                      {ep.summary && (
                        <p className="episode-summary">{ep.summary.replace(/<[^>]*>/g, '')}</p>
                      )}
                      <div className="episode-insight">
                        <AIInsight showId={showId} episodeId={ep.id} />
                      </div>
                      <div className="episode-comments">
                        <Comments showId={showId} episodeId={ep.id} />
                      </div>
                    </>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}
