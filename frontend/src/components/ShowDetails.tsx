import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { ShowWithEpisodes } from '../types';
import { SeasonList } from './SeasonList';
import { AIInsight } from './AIInsight';
import { Comments } from './Comments';

type ShowDetailsProps = {
  showId: number;
  onBack: () => void;
}

export function ShowDetails({ showId, onBack }: ShowDetailsProps) {
  const [show, setShow] = useState<ShowWithEpisodes | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDetails = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.getShowDetails(showId);
        setShow(data);
      } catch (err) {
        setError('Failed to load show details');
      } finally {
        setLoading(false);
      }
    };
    fetchDetails();
  }, [showId]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!show) return <div className="error">Show not found</div>;


  return (
    <div className="show-details">
      <button onClick={onBack} className="back-button">← Back</button>
      
      <div className="show-header">
        {show.poster_url && (
          <img src={show.poster_url} alt={show.name} className="show-poster-large" />
        )}
        <div className="show-info">
          <h1>{show.name}</h1>
          {show.year && <p className="year">{show.year}</p>}
          {show.genres.length > 0 && (
            <div className="genres">
              {show.genres.map(genre => (
                <span key={genre} className="genre-tag">{genre}</span>
              ))}
            </div>
          )}
          {show.summary && <p className="summary">{show.summary.replace(/<[^>]*>/g, '')}</p>}
          <AIInsight showId={show.id} />
        </div>
      </div>

      <div className="episodes-section">
        <h2>Episodes</h2>
        {show.seasons.length === 0 ? (
          <p>No episodes available</p>
        ) : (
          <SeasonList seasons={show.seasons} showId={show.id} />
        )}
      </div>

      <Comments showId={show.id} />
    </div>
  );
}