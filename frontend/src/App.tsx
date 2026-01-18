import { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import type { ShowSearchResult } from './types';
import './App.css';

function App() {
  const [selectedShow, setSelectedShow] = useState<ShowSearchResult | null>(null);

  return (
    <div className="app">
      <header className="app-header">
        <h1>TV Series Explorer</h1>
      </header>

      <main className="app-main">
        <SearchBar onSelectShow={setSelectedShow} />

        {selectedShow && (
          <div className="selected-show">
            <h2>Selected: {selectedShow.name}</h2>
            {selectedShow.poster_url && (
              <img src={selectedShow.poster_url} alt={selectedShow.name} className="show-poster" />
            )}
            <p>Year: {selectedShow.year || 'Unknown'}</p>
            <p className="hint">Show details page coming soon!</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;