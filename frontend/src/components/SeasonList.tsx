import { useState } from 'react';
import type { Season } from '../types';
import { AIInsight } from './AIInsight';
import { Comments } from './Comments';

export function SeasonList({ seasons, showId }: { seasons: Season[]; showId: number }) {
  const [expandedSeason, setExpandedSeason] = useState<number | null>(1);
  const [expandedEpisode, setExpandedEpisode] = useState<number | null>(null);

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
                <li key={ep.id} className="episode-item">
                  <div 
                    className="episode-header"
                    onClick={() => setExpandedEpisode(expandedEpisode === ep.id ? null : ep.id)}
                    style={{ cursor: 'pointer' }}
                  >
                    <span className="episode-number">{ep.number}</span>
                    <span className="episode-name">{ep.name}</span>
                    {ep.airdate && <span className="episode-airdate">{ep.airdate}</span>}
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
