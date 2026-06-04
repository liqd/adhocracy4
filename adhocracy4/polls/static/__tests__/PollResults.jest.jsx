import React from 'react'
import { render, screen } from '@testing-library/react'
import PollResults from '../PollDetail/PollResults.jsx'

jest.mock('react-slick', () => {
  return function MockSlider ({ children }) {
    return <div data-testid="mock-slider">{children}</div>
  }
})

describe('<PollResults> confidential', () => {
  test('shows only response count for confidential open question', () => {
    const question = {
      id: 1,
      label: 'Contact details',
      is_open: true,
      is_confidential: true,
      multiple_choice: false,
      choices: [],
      userChoices: [],
      answers: [],
      totalAnswerCount: 15,
      totalVoteCount: 0,
      totalVoteCountMulti: 0,
      other_choice_answers: []
    }

    const { container } = render(<PollResults question={question} />)

    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Contact details')
    expect(container.querySelector('.poll--confidential')).toBeInTheDocument()
    expect(screen.getByText(/response submitted/i)).toBeInTheDocument()
    expect(screen.queryByRole('region', { name: /open answers carousel/i })).not.toBeInTheDocument()
  })

  test('shows only response count for confidential choice question', () => {
    const question = {
      id: 2,
      label: 'Sensitive choice',
      is_open: false,
      is_confidential: true,
      multiple_choice: false,
      choices: [{ id: 1, label: 'A', count: 0, is_other_choice: false }],
      userChoices: [1],
      answers: [],
      totalAnswerCount: 0,
      totalVoteCount: 8,
      totalVoteCountMulti: 8,
      other_choice_answers: []
    }

    const { container } = render(<PollResults question={question} />)

    expect(container.querySelector('.poll--confidential')).toBeInTheDocument()
    expect(screen.getByText(/response submitted/i)).toBeInTheDocument()
    expect(screen.queryByText('%')).not.toBeInTheDocument()
  })
})
