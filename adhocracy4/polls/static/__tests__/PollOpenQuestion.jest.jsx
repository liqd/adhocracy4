import React from 'react'
import { render, screen } from '@testing-library/react'
import { PollOpenQuestion } from '../PollDetail/PollOpenQuestion.jsx'

const question = {
  id: 1,
  label: 'Your thoughts',
  help_text: '',
  is_open: true,
  is_confidential: false,
  isReadOnly: false,
  authenticated: true,
  userAnswer: '',
  answers: []
}

const renderQuestion = (override = {}) => render(
  <PollOpenQuestion
    question={{ ...question, ...override }}
    allowUnregisteredUsers={false}
    onOpenChange={() => {}}
    errors={{}}
  />
)

describe('mandatory questions when answering', () => {
  test('marks a mandatory question with an asterisk', () => {
    const { container } = renderQuestion({ is_mandatory: true })

    const marker = container.querySelector('.poll__question-required')
    expect(marker).toHaveTextContent('*')
    expect(marker).toHaveAttribute('aria-hidden', 'true')
    expect(screen.getByText('Mandatory question')).toBeInTheDocument()
  })

  test('does not mark an optional question', () => {
    const { container } = renderQuestion()

    expect(container.querySelector('.poll__question-required')).not.toBeInTheDocument()
  })

  test('marks the answer field of a mandatory question as required', () => {
    const { container } = renderQuestion({ is_mandatory: true })

    expect(container.querySelector('textarea')).toHaveAttribute('aria-required', 'true')
  })

  test('does not mark the answer field of an optional question as required', () => {
    const { container } = renderQuestion()

    expect(container.querySelector('textarea')).not.toHaveAttribute('aria-required')
  })
})
