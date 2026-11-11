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

import QuestionFunnel from '../PollDetail/QuestionFunnel'

describe('QuestionFunnel', () => {
  beforeEach(() => {
    window.scrollTo = jest.fn()
  })

  const choiceQuestion = {
    id: 1,
    label: 'Favorite color',
    is_open: false,
    multiple_choice: false,
    is_confidential: false,
    authenticated: true,
    choices: [
      { id: 10, label: 'Red', is_other_choice: false },
      { id: 11, label: 'Blue', is_other_choice: false }
    ]
  }

  const openQuestion = {
    id: 2,
    label: 'Your thoughts',
    is_open: true,
    authenticated: true,
    multiple_choice: false,
    choices: [],
    answers: [],
    userAnswer: null
  }

  const baseProps = {
    currentQuestion: choiceQuestion,
    currentAnswer: null,
    currentNumber: 1,
    totalQuestions: 3,
    allowUnregisteredUsers: false,
    useTermsOfUse: false,
    agreedTermsOfUse: false,
    orgTermsUrl: '',
    checkedTermsOfUse: false,
    showCaptcha: false,
    captcha: '',
    onSetCheckedTerms: jest.fn(),
    errors: {},
    onAnswerChange: jest.fn(),
    onBack: jest.fn(),
    onSkip: jest.fn(),
    onNext: jest.fn(),
    onSubmit: jest.fn(),
    isLoading: false,
    questionImagesEnabled: false
  }

  it('renders the question header with numbering', () => {
    render(<QuestionFunnel {...baseProps} currentNumber={1} totalQuestions={3} />)
    expect(screen.getByText('Question 1 of 3')).toBeInTheDocument()
  })

  it('renders the progress bar', () => {
    render(<QuestionFunnel {...baseProps} currentNumber={3} totalQuestions={5} />)
    const bar = screen.getByRole('progressbar')
    expect(bar).toHaveAttribute('aria-valuenow', '60')
    expect(bar).toHaveStyle({ width: '60%' })
  })

  it('renders PollChoice for non-open questions', () => {
    render(<QuestionFunnel {...baseProps} />)
    expect(screen.getByText('Favorite color')).toBeInTheDocument()
    expect(screen.getByText('Red')).toBeInTheDocument()
    expect(screen.getByText('Blue')).toBeInTheDocument()
  })

  it('renders PollOpenQuestion for open questions', () => {
    render(<QuestionFunnel {...baseProps} currentQuestion={openQuestion} />)
    expect(screen.getByTestId('poll-open-question')).toBeInTheDocument()
  })

  it('calls onNext, onBack and onSkip', () => {
    const onNext = jest.fn()
    const onBack = jest.fn()
    const onSkip = jest.fn()
    render(
      <QuestionFunnel
        {...baseProps}
        currentNumber={2}
        totalQuestions={3}
        onNext={onNext}
        onBack={onBack}
        onSkip={onSkip}
      />
    )
    fireEvent.click(screen.getByText('Next'))
    fireEvent.click(screen.getByText('Go Back'))
    fireEvent.click(screen.getByText('Skip'))
    expect(onNext).toHaveBeenCalledTimes(1)
    expect(onBack).toHaveBeenCalledTimes(1)
    expect(onSkip).toHaveBeenCalledTimes(1)
  })

  it('shows Submit All and calls onSubmit on the last question', () => {
    const onSubmit = jest.fn()
    render(<QuestionFunnel {...baseProps} currentNumber={3} totalQuestions={3} onSubmit={onSubmit} />)
    expect(screen.getByText('Submit All')).toBeInTheDocument()
    fireEvent.click(screen.getByText('Submit All'))
    expect(onSubmit).toHaveBeenCalledTimes(1)
  })

  it('shows Submitting... when loading on the last question', () => {
    render(<QuestionFunnel {...baseProps} currentNumber={3} totalQuestions={3} isLoading />)
    expect(screen.getByText('Submitting...')).toBeDisabled()
  })

  it('renders the current question read-only while submitting', () => {
    render(<QuestionFunnel {...baseProps} currentNumber={3} totalQuestions={3} isLoading />)
    const input = screen.getByText('Red').closest('label').querySelector('input')
    expect(input).toBeDisabled()
  })

  it('enriches the question with the current answer and forwards changes', () => {
    const onAnswerChange = jest.fn()
    render(
      <QuestionFunnel
        {...baseProps}
        currentAnswer={{ choices: [10], open_answer: '', other_choice_answer: '' }}
        onAnswerChange={onAnswerChange}
      />
    )
    expect(screen.getByText('Red').closest('label').querySelector('input')).toBeChecked()
    fireEvent.click(screen.getByText('Blue'))
    expect(onAnswerChange).toHaveBeenCalledWith(1, { choices: [11] })
  })

  it('forwards open question answer changes', () => {
    const onAnswerChange = jest.fn()
    render(
      <QuestionFunnel
        {...baseProps}
        currentQuestion={openQuestion}
        onAnswerChange={onAnswerChange}
      />
    )
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'My answer' } })
    expect(onAnswerChange).toHaveBeenCalledWith(2, { open_answer: 'My answer' })
  })
})
