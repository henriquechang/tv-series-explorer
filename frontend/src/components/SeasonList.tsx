import { useState } from 'react';
import type { Season } from '../types';

export function SeasonList({ seasons }: { seasons: Season[] }) {
  const [expandedSeason, setExpandedSeason] = useState<number | null>(1);

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
                  <div className="episode-header">
                    <span className="episode-number">{ep.number}</span>
                    <span className="episode-name">{ep.name}</span>
                    {ep.airdate && <span className="episode-airdate">{ep.airdate}</span>}
                  </div>
                  {ep.summary && (
                    <p className="episode-summary">{ep.summary.replace(/<[^>]*>/g, '')}</p>
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
