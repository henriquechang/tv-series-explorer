import { useState, useEffect } from 'react';
import { useDebounce } from '../hooks/useDebounce';
import { api } from '../services/api';
import type { ShowSearchResult } from '../types';

interface SearchBarProps {
  onSelectShow: (show: ShowSearchResult) => void;
}

export function SearchBar({ onSelectShow }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<ShowSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (!debouncedQuery) {
      setResults([]);
      return;
    }

    const search = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await api.searchShows(debouncedQuery);
        setResults(data);
      } catch (err) {
        setError('Failed to search. Please try again.');
        setResults([]);
      } finally {
        setLoading(false);
      }
    };

    search();
  }, [debouncedQuery]);

  const handleSelect = (show: ShowSearchResult) => {
    onSelectShow(show);
    setQuery('');
    setResults([]);
  };

  return (
    <div className="search-container">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search TV shows..."
        className="search-input"
      />
      
      {loading && <div className="search-loading">Searching...</div>}
      {error && <div className="search-error">{error}</div>}
      
      {results.length > 0 && (
        <ul className="search-results">
          {results.map((show) => (
            <li key={show.id} onClick={() => handleSelect(show)} className="search-result-item">
              {show.poster_url && (
                <img src={show.poster_url} alt={show.name} className="search-result-poster" />
              )}
              <div className="search-result-info">
                <span className="search-result-name">{show.name}</span>
                {show.year && <span className="search-result-year">({show.year})</span>}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}