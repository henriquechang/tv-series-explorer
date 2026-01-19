import { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { ShowDetails } from './components/ShowDetails';
import type { ShowSearchResult } from './types';
import './App.css';

function App() {
  const [selectedShowId, setSelectedShowId] = useState<number | null>(null);

  const handleSelectShow = (show: ShowSearchResult) => {
    setSelectedShowId(show.id);
  };

  const handleBack = () => {
    setSelectedShowId(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 onClick={handleBack} style={{ cursor: 'pointer' }}>TV Series Explorer</h1>
      </header>

      <main className="app-main">
        {selectedShowId === null ? (
          <SearchBar onSelectShow={handleSelectShow} />
        ) : (
          <ShowDetails showId={selectedShowId} onBack={handleBack} />
        )}
      </main>
    </div>
  );
}

export default App;