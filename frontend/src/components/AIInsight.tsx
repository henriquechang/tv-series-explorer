import { useState } from 'react';
import { api } from '../services/api';

interface AIInsightProps {
  showId: number;
  episodeId?: number;
}

export function AIInsight({ showId, episodeId }: AIInsightProps) {
  const [insight, setInsight] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchInsight = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = episodeId
        ? await api.getEpisodeInsight(showId, episodeId)
        : await api.getShowInsight(showId);
      setInsight(data.insight);
    } catch (err) {
      setError('Failed to generate insight');
    } finally {
      setLoading(false);
    }
  };

  if (!insight && !loading && !error) {
    return (
      <button onClick={fetchInsight} className="insight-button">
        View insight
      </button>
    );
  }

  return (
    <div className="ai-insight">
      {loading && <span className="insight-loading">Loading...</span>}
      {error && <span className="insight-error">{error}</span>}
      {insight && (
        <div className="insight-content">
          <p className="insight-text">{insight}</p>
          <button onClick={fetchInsight} className="refresh-button">
            Refresh
          </button>
        </div>
      )}
    </div>
  );
}