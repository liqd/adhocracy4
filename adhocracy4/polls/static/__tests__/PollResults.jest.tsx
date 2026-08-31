import React from 'react'
import { render, screen } from '@testing-library/react'
import PollResults from '../PollDetail/PollResults'
import type { PollQuestion } from '../../../static/api/types'

jest.mock('react-slick', () => {
  return function MockSlider ({ children }: { children: React.ReactNode }) {
    return <div data-testid="mock-slider">{children}</div>
  }
})

describe('<PollResults> confidential', () => {
  const baseQuestion: PollQuestion = {
    id: 0,
    label: '',
    help_text: '',
    is_open: false,
    is_confidential: false,
    multiple_choice: false,
    isReadOnly: false,
    authenticated: false,
    image_url: null,
    image_alt_text: '',
    image_help_text: '',
    choices: [],
    userChoices: [],
    answers: [],
    other_choice_answers: [],
    other_choice_user_answer: '',
    userAnswer: '',
    totalVoteCount: 0,
    totalVoteCountMulti: 0,
    totalAnswerCount: 0
  }

  test('shows only response count for confidential open question', () => {
    const question: PollQuestion = {
      ...baseQuestion,
      id: 1,
      label: 'Contact details',
      is_open: true,
      is_confidential: true,
      totalAnswerCount: 15
    }

    const { container } = render(<PollResults question={question} />)

    expect(screen.getByRole('heading', { level: 2 })).toHaveTextContent('Contact details')
    expect(container.querySelector('.poll--confidential')).toBeInTheDocument()
    expect(screen.getByText(/response submitted/i)).toBeInTheDocument()
    expect(screen.queryByRole('region', { name: /open answers carousel/i })).not.toBeInTheDocument()
  })

  test('shows only response count for confidential choice question', () => {
    const question: PollQuestion = {
      ...baseQuestion,
      id: 2,
      label: 'Sensitive choice',
      is_confidential: true,
      choices: [{ id: 1, label: 'A', count: 0, is_other_choice: false }],
      userChoices: [1],
      totalVoteCount: 8,
      totalVoteCountMulti: 8
    }

    const { container } = render(<PollResults question={question} />)

    expect(container.querySelector('.poll--confidential')).toBeInTheDocument()
    expect(screen.getByText(/response submitted/i)).toBeInTheDocument()
    expect(screen.queryByText('%')).not.toBeInTheDocument()
  })
})