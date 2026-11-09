import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

jest.mock('django', () => ({
  gettext: (text) => text,
  pgettext: (context, text) => text,
  ngettext: (singular, plural, count) => count === 1 ? singular : plural,
  interpolate: (fmt, data, named) => {
    if (named) {
      return fmt.replace(/%\((\w+)\)s/g, (match, key) => data[key])
    }
    return fmt
  }
}))

import StartScreen from '../PollDetail/StartScreen'

describe('StartScreen', () => {
  beforeEach(() => {
    window.adhocracy4 = { getCurrentPath: () => '/poll' }
  })

  const baseProps = {
    totalQuestions: 2,
    totalParticipants: 5,
    isAuthenticated: true,
    allowUnregisteredUsers: false,
    canVote: true,
    hideResultsUntilFinished: false,
    manualLink: '',
    onStart: jest.fn(),
    onShowResults: jest.fn()
  }

  it('shows the results button by default', () => {
    render(<StartScreen {...baseProps} />)
    expect(screen.getByText('Show results')).toBeInTheDocument()
  })

  it('hides the results button when results are hidden until the phase ends', () => {
    render(<StartScreen {...baseProps} hideResultsUntilFinished />)
    expect(screen.queryByText('Show results')).not.toBeInTheDocument()
  })

  it('starts the poll', () => {
    const onStart = jest.fn()
    render(<StartScreen {...baseProps} onStart={onStart} />)
    fireEvent.click(screen.getByText('Start'))
    expect(onStart).toHaveBeenCalledTimes(1)
  })

  it('shows the login link when participation is not possible', () => {
    render(<StartScreen {...baseProps} isAuthenticated={false} allowUnregisteredUsers={false} canVote={false} />)
    expect(screen.getByText('Log in to participate')).toBeInTheDocument()
  })

  it('lets anonymous users start when unregistered voting is allowed', () => {
    render(<StartScreen {...baseProps} isAuthenticated={false} allowUnregisteredUsers canVote />)
    expect(screen.getByText('Start')).toBeInTheDocument()
  })

  it('does not offer start or login to authenticated users without permission', () => {
    render(<StartScreen {...baseProps} isAuthenticated canVote={false} />)
    expect(screen.queryByText('Start')).not.toBeInTheDocument()
    expect(screen.queryByText('Log in to participate')).not.toBeInTheDocument()
  })
})
