import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ShowDetails } from './ShowDetails'
import { api } from '../services/api'

vi.mock('../services/api')
vi.mock('./SeasonList', () => ({
  SeasonList: vi.fn(() => <div>Season List</div>)
}))

describe('ShowDetails', () => {
  const mockBack = vi.fn()
  const mockShowData = {
    id: 1,
    name: 'Breaking Bad',
    year: 2008,
    poster_url: 'https://example.com/poster.jpg',
    genres: ['Drama', 'Crime'],
    summary: '<p>Test</p>',
    seasons: [
      {
        season_number: 1,
        episodes: [
          { id: 1, season: 1, name: 'Pilot', number: 1, airdate: '2008-01-20', summary: null }
        ]
      }
    ]
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows loading', () => {
    vi.mocked(api.getShowDetails).mockImplementation(() => new Promise(() => {}))
    render(<ShowDetails showId={1} onBack={mockBack} />)
    expect(screen.getByText('Loading...')).toBeInTheDocument()
  })

  it('shows the show', async () => {
    vi.mocked(api.getShowDetails).mockResolvedValue(mockShowData)
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      expect(screen.getByText('Breaking Bad')).toBeInTheDocument()
      expect(screen.getByText('2008')).toBeInTheDocument()
      expect(screen.getByText('Drama')).toBeInTheDocument()
      expect(screen.getByText('Crime')).toBeInTheDocument()
      expect(screen.getByText('Test')).toBeInTheDocument()
    })
  })

  it('shows poster', async () => {
    vi.mocked(api.getShowDetails).mockResolvedValue(mockShowData)
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      const img = screen.getByAltText('Breaking Bad')
      expect(img).toHaveAttribute('src', 'https://example.com/poster.jpg')
    })
  })

  it('removes html tags', async () => {
    vi.mocked(api.getShowDetails).mockResolvedValue(mockShowData)
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      expect(screen.queryByText(/<p>/)).not.toBeInTheDocument()
      expect(screen.getByText('Test')).toBeInTheDocument()
    })
  })

  it('back button works', async () => {
    vi.mocked(api.getShowDetails).mockResolvedValue(mockShowData)
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      expect(screen.getByText('← Back')).toBeInTheDocument()
    })

    await userEvent.click(screen.getByText('← Back'))
    expect(mockBack).toHaveBeenCalledOnce()
  })

  it('shows error', async () => {
    vi.mocked(api.getShowDetails).mockRejectedValue(new Error('oops'))
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      expect(screen.getByText('Failed to load show details')).toBeInTheDocument()
    })
  })

  it('handles no episodes', async () => {
    vi.mocked(api.getShowDetails).mockResolvedValue({
      ...mockShowData,
      seasons: []
    })
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      expect(screen.getByText('No episodes available')).toBeInTheDocument()
    })
  })

  it('shows seasons', async () => {
    vi.mocked(api.getShowDetails).mockResolvedValue(mockShowData)
    render(<ShowDetails showId={1} onBack={mockBack} />)

    await waitFor(() => {
      expect(screen.getByText('Season List')).toBeInTheDocument()
    })
  })
})