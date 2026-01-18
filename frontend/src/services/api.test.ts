import { describe, it, expect, vi, beforeEach } from 'vitest'
import { api } from './api'

describe('api', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('handles single character queries', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([])
    }))
    
    await api.searchShows('a')
    expect(fetch).toHaveBeenCalledWith('/api/shows/search?q=a')
  })

  it('searches for shows', async () => {
    const mockShows = [
      { id: 1, name: 'Breaking Bad', year: 2008, poster_url: 'https://example.com/bb.jpg' },
      { id: 82, name: 'Game of Thrones', year: 2011, poster_url: null }
    ]

    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockShows)
    }))

    const results = await api.searchShows('breaking bad')
    
    expect(fetch).toHaveBeenCalledWith('/api/shows/search?q=breaking%20bad')
    expect(results).toEqual(mockShows)
  })

  it('handles server errors', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 500
    }))

    await expect(api.searchShows('the office')).rejects.toThrow('HTTP 500')
  })

  it('handles spaces in search queries', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([])
    }))

    await api.searchShows('the wire')
    expect(fetch).toHaveBeenCalledWith('/api/shows/search?q=the%20wire')
  })
})