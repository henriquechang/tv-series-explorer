import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SearchBar } from './SearchBar'
import { api } from '../services/api'

vi.mock('../services/api')

describe('SearchBar', () => {
  const mockSelect = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders search input', () => {
    render(<SearchBar onSelectShow={mockSelect} />)
    expect(screen.getByPlaceholderText('Search TV shows...')).toBeInTheDocument()
  })

  it('calls api when typing', async () => {
    vi.mocked(api.searchShows).mockResolvedValue([])
    render(<SearchBar onSelectShow={mockSelect} />)

    await userEvent.type(screen.getByPlaceholderText('Search TV shows...'), 'breaking bad')

    await waitFor(() => {
      expect(api.searchShows).toHaveBeenCalledWith('breaking bad')
    })
  })

  it('shows results', async () => {
    vi.mocked(api.searchShows).mockResolvedValue([
      { id: 1, name: 'Breaking Bad', year: 2008, poster_url: null }
    ])
    render(<SearchBar onSelectShow={mockSelect} />)

    await userEvent.type(screen.getByPlaceholderText('Search TV shows...'), 'test')

    await waitFor(() => {
      expect(screen.getByText('Breaking Bad')).toBeInTheDocument()
      expect(screen.getByText('(2008)')).toBeInTheDocument()
    })
  })

  it('handles clicks', async () => {
    const show = { id: 1, name: 'Test Show', year: 2020, poster_url: null }
    vi.mocked(api.searchShows).mockResolvedValue([show])
    render(<SearchBar onSelectShow={mockSelect} />)

    await userEvent.type(screen.getByPlaceholderText('Search TV shows...'), 'test')
    
    await waitFor(() => {
      expect(screen.getByText('Test Show')).toBeInTheDocument()
    })

    await userEvent.click(screen.getByText('Test Show'))
    expect(mockSelect).toHaveBeenCalledWith(show)
  })

  it('shows error message', async () => {
    vi.mocked(api.searchShows).mockRejectedValue(new Error('oops'))
    render(<SearchBar onSelectShow={mockSelect} />)

    await userEvent.type(screen.getByPlaceholderText('Search TV shows...'), 'test')

    await waitFor(() => {
      expect(screen.getByText('Failed to search. Please try again.')).toBeInTheDocument()
    })
  })
})