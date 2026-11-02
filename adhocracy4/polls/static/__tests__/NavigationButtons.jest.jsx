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

import NavigationButtons from '../PollDetail/NavigationButtons'

describe('NavigationButtons', () => {
  const defaults = {
    onBack: jest.fn(),
    onSkip: jest.fn(),
    onNext: jest.fn(),
    onSubmit: jest.fn(),
    isLoading: false,
    isLastQuestion: false,
    isSubmitDisabled: false,
    currentIndex: 0
  }

  it('disables Back on the first question', () => {
    render(<NavigationButtons {...defaults} currentIndex={0} />)
    expect(screen.getByText('Go Back')).toBeDisabled()
  })

  it('enables Back after the first question', () => {
    render(<NavigationButtons {...defaults} currentIndex={1} />)
    expect(screen.getByText('Go Back')).not.toBeDisabled()
  })

  it('shows Skip and Next on non-last questions', () => {
    render(<NavigationButtons {...defaults} isLastQuestion={false} />)
    expect(screen.getByText('Skip')).toBeInTheDocument()
    expect(screen.getByText('Next')).toBeInTheDocument()
    expect(screen.queryByText('Submit All')).not.toBeInTheDocument()
  })

  it('shows Submit All on the last question and hides Skip/Next', () => {
    render(<NavigationButtons {...defaults} isLastQuestion />)
    expect(screen.getByText('Submit All')).toBeInTheDocument()
    expect(screen.queryByText('Skip')).not.toBeInTheDocument()
    expect(screen.queryByText('Next')).not.toBeInTheDocument()
  })

  it('shows Submitting... and disables the button when loading', () => {
    render(<NavigationButtons {...defaults} isLastQuestion isLoading />)
    expect(screen.getByText('Submitting...')).toBeDisabled()
  })

  it('calls the back, skip and next handlers', () => {
    const onBack = jest.fn()
    const onSkip = jest.fn()
    const onNext = jest.fn()
    render(
      <NavigationButtons
        {...defaults}
        currentIndex={1}
        onBack={onBack}
        onSkip={onSkip}
        onNext={onNext}
      />
    )
    fireEvent.click(screen.getByText('Go Back'))
    fireEvent.click(screen.getByText('Skip'))
    fireEvent.click(screen.getByText('Next'))
    expect(onBack).toHaveBeenCalledTimes(1)
    expect(onSkip).toHaveBeenCalledTimes(1)
    expect(onNext).toHaveBeenCalledTimes(1)
  })

  it('calls onSubmit when Submit All is clicked', () => {
    const onSubmit = jest.fn()
    render(<NavigationButtons {...defaults} isLastQuestion onSubmit={onSubmit} />)
    fireEvent.click(screen.getByText('Submit All'))
    expect(onSubmit).toHaveBeenCalledTimes(1)
  })
})
