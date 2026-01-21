import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import { AIInsight } from './AIInsight';
import { api } from '../services/api';

vi.mock('../services/api');

describe('AIInsight Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders View insight button initially', () => {
    render(<AIInsight showId={1} />);
    expect(screen.getByRole('button', { name: /view insight/i })).toBeInTheDocument();
  });

  it('shows loading state when fetching insight', async () => {
    vi.mocked(api.getShowInsight).mockImplementation(() => new Promise(() => {}));

    render(<AIInsight showId={1} />);
    fireEvent.click(screen.getByRole('button', { name: /view insight/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  it('displays show insight when successfully fetched', async () => {
    const mockInsight = {
      insight: 'This show offers compelling storytelling and great characters.',
      source: 'ai'
    };
    
    vi.mocked(api.getShowInsight).mockResolvedValue(mockInsight);

    render(<AIInsight showId={1} />);
    fireEvent.click(screen.getByRole('button', { name: /view insight/i }));
    
    await waitFor(() => {
      expect(screen.getByText(mockInsight.insight)).toBeInTheDocument();
    });
    
    expect(screen.getByRole('button', { name: /refresh/i })).toBeInTheDocument();
  });

  it('displays episode insight when episodeId is provided', async () => {
    const mockInsight = {
      insight: 'This episode sets the stage for the series.',
      source: 'ai'
    };
    
    vi.mocked(api.getEpisodeInsight).mockResolvedValue(mockInsight);

    render(<AIInsight showId={1} episodeId={101} />);
    fireEvent.click(screen.getByRole('button', { name: /view insight/i }));
    
    await waitFor(() => {
      expect(screen.getByText(mockInsight.insight)).toBeInTheDocument();
    });
    
    expect(api.getEpisodeInsight).toHaveBeenCalledWith(1, 101);
    expect(api.getShowInsight).not.toHaveBeenCalled();
  });

  it('displays error message when fetching fails', async () => {
    vi.mocked(api.getShowInsight).mockRejectedValue(new Error('Network error'));

    render(<AIInsight showId={1} />);
    fireEvent.click(screen.getByRole('button', { name: /view insight/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Failed to generate insight')).toBeInTheDocument();
    });
  });

  it('allows refreshing the insight', async () => {
    const firstInsight = { insight: 'First insight about the show.', source: 'ai' };
    const secondInsight = { insight: 'Updated insight about the show.', source: 'ai' };
    
    vi.mocked(api.getShowInsight)
      .mockResolvedValueOnce(firstInsight)
      .mockResolvedValueOnce(secondInsight);

    render(<AIInsight showId={1} />);
    
    fireEvent.click(screen.getByRole('button', { name: /view insight/i }));
    await waitFor(() => {
      expect(screen.getByText(firstInsight.insight)).toBeInTheDocument();
    });
    
    fireEvent.click(screen.getByRole('button', { name: /refresh/i }));
    await waitFor(() => {
      expect(screen.getByText(secondInsight.insight)).toBeInTheDocument();
    });
    
    expect(api.getShowInsight).toHaveBeenCalledTimes(2);
  });
});