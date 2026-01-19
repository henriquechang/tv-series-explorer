import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SeasonList } from './SeasonList'

describe('SeasonList', () => {
  const mockSeasons = [
    {
      season_number: 1,
      episodes: [
        { id: 1, season: 1, name: 'Pilot', number: 1, airdate: '2008-01-20', summary: '<p>First episode</p>' },
        { id: 2, season: 1, name: 'Cat Bag', number: 2, airdate: '2008-01-27', summary: null }
      ]
    },
    {
      season_number: 2,
      episodes: [
        { id: 3, season: 2, name: 'Test', number: 1, airdate: '2009-03-08', summary: '<p>Season 2 starts</p>' }
      ]
    }
  ]

  it('shows all seasons', () => {
    render(<SeasonList seasons={mockSeasons} />)
    expect(screen.getByText('Season 1')).toBeInTheDocument()
    expect(screen.getByText('Season 2')).toBeInTheDocument()
  })

  it('shows episode count', () => {
    render(<SeasonList seasons={mockSeasons} />)
    expect(screen.getByText('2 episodes')).toBeInTheDocument()
    expect(screen.getByText('1 episodes')).toBeInTheDocument()
  })

  it('expands first season by default', () => {
    render(<SeasonList seasons={mockSeasons} />)
    expect(screen.getByText('Pilot')).toBeInTheDocument()
    expect(screen.getByText('Cat Bag')).toBeInTheDocument()
  })

  it('toggles seasons', async () => {
    render(<SeasonList seasons={mockSeasons} />)

    expect(screen.queryByText('Test')).not.toBeInTheDocument()
    
    await userEvent.click(screen.getByText('Season 2'))
    expect(screen.getByText('Test')).toBeInTheDocument()
    
    await userEvent.click(screen.getByText('Season 2'))
    expect(screen.queryByText('Test')).not.toBeInTheDocument()
  })

  it('shows episode details', () => {
    render(<SeasonList seasons={mockSeasons} />)
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
    expect(screen.getByText('2008-01-20')).toBeInTheDocument()
  })

  it('shows episode summary', () => {
    render(<SeasonList seasons={mockSeasons} />)
    expect(screen.getByText('First episode')).toBeInTheDocument()
  })

  it('removes html from summary', () => {
    render(<SeasonList seasons={mockSeasons} />)
    expect(screen.queryByText(/<p>/)).not.toBeInTheDocument()
    expect(screen.getByText('First episode')).toBeInTheDocument()
  })

  it('handles empty seasons', () => {
    render(<SeasonList seasons={[]} />)
    expect(screen.queryByText('Season')).not.toBeInTheDocument()
  })

  it('handles episodes without summary', () => {
    render(<SeasonList seasons={mockSeasons} />)
    const catBagElem = screen.getByText('Cat Bag').parentElement
    expect(catBagElem?.parentElement?.querySelector('.episode-summary')).not.toBeInTheDocument()
  })
})