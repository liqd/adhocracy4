import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

import { PollChoice } from '../PollDetail/PollChoice'

describe('PollChoice', () => {
  const singleQuestion = {
    id: 1,
    label: 'Pick one',
    multiple_choice: false,
    is_open: false,
    is_confidential: false,
    authenticated: true,
    choices: [
      { id: 10, label: 'Red', is_other_choice: false },
      { id: 11, label: 'Blue', is_other_choice: false }
    ],
    userChoices: []
  }

  const multiQuestion = {
    ...singleQuestion,
    label: 'Pick many',
    multiple_choice: true,
    choices: [
      { id: 10, label: 'Red', is_other_choice: false },
      { id: 11, label: 'Blue', is_other_choice: false },
      { id: 12, label: 'other', is_other_choice: true }
    ]
  }

  it('renders the question label', () => {
    render(<PollChoice question={singleQuestion} allowUnregisteredUsers={false} onAnswerChange={jest.fn()} />)
    expect(screen.getByText('Pick one')).toBeInTheDocument()
  })

  it('renders radio inputs for single choice', () => {
    const { container } = render(<PollChoice question={singleQuestion} allowUnregisteredUsers={false} onAnswerChange={jest.fn()} />)
    expect(container.querySelectorAll('input[type="radio"]')).toHaveLength(2)
  })

  it('renders checkbox inputs for multiple choice', () => {
    const { container } = render(<PollChoice question={multiQuestion} allowUnregisteredUsers={false} onAnswerChange={jest.fn()} />)
    expect(container.querySelectorAll('input[type="checkbox"]')).toHaveLength(3)
  })

  it('calls onAnswerChange with single type on radio click', () => {
    const onAnswerChange = jest.fn()
    render(<PollChoice question={singleQuestion} allowUnregisteredUsers={false} onAnswerChange={onAnswerChange} />)
    fireEvent.click(screen.getByText('Red'))
    expect(onAnswerChange).toHaveBeenCalledWith(1, 10, 'single')
  })

  it('calls onAnswerChange with multi type on checkbox click', () => {
    const onAnswerChange = jest.fn()
    render(<PollChoice question={multiQuestion} allowUnregisteredUsers={false} onAnswerChange={onAnswerChange} />)
    fireEvent.click(screen.getByText('Red'))
    expect(onAnswerChange).toHaveBeenCalledWith(1, 10, 'multi')
  })

  it('shows the textarea when the other choice is selected', () => {
    const { rerender } = render(
      <PollChoice question={multiQuestion} allowUnregisteredUsers={false} onAnswerChange={jest.fn()} />
    )
    fireEvent.click(screen.getByText('other'))
    rerender(
      <PollChoice
        question={{ ...multiQuestion, userChoices: [12] }}
        allowUnregisteredUsers={false}
        onAnswerChange={jest.fn()}
      />
    )
    expect(screen.getByTestId('textarea-with-counter')).toBeInTheDocument()
  })

  it('shows the multiple choice help text', () => {
    render(<PollChoice question={multiQuestion} allowUnregisteredUsers={false} onAnswerChange={jest.fn()} />)
    expect(screen.getByText('Multiple answers are possible.')).toBeInTheDocument()
  })

  it('renders the question image with alt text', () => {
    const { container } = render(
      <PollChoice
        question={{
          ...singleQuestion,
          image_url: 'http://example.com/image.jpg',
          image_alt_text: 'Descriptive image text'
        }}
        allowUnregisteredUsers={false}
        onAnswerChange={jest.fn()}
        questionImagesEnabled
      />
    )
    const img = container.querySelector('.poll__question-image-img')
    expect(img).toHaveAttribute('alt', 'Descriptive image text')
  })

  it('does not render the image when images are disabled', () => {
    const { container } = render(
      <PollChoice
        question={{
          ...singleQuestion,
          image_url: 'http://example.com/image.jpg',
          image_alt_text: 'Descriptive image text'
        }}
        allowUnregisteredUsers={false}
        onAnswerChange={jest.fn()}
        questionImagesEnabled={false}
      />
    )
    expect(container.querySelector('.poll__question-image')).not.toBeInTheDocument()
  })
})

describe('mandatory choice questions', () => {
  const mandatoryQuestion = {
    id: 1,
    label: 'Pick one',
    multiple_choice: false,
    is_open: false,
    is_confidential: false,
    authenticated: true,
    is_mandatory: true,
    choices: [
      { id: 10, label: 'Red', is_other_choice: false },
      { id: 11, label: 'Blue', is_other_choice: false }
    ],
    userChoices: []
  }

  it('marks a mandatory question with an asterisk and required inputs', () => {
    const { container } = render(
      <PollChoice
        question={mandatoryQuestion}
        allowUnregisteredUsers={false}
        onAnswerChange={jest.fn()}
      />
    )

    const marker = container.querySelector('.poll__question-required')
    expect(marker).toHaveTextContent('*')
    expect(marker).toHaveAttribute('aria-hidden', 'true')
    expect(screen.getByText('Mandatory question')).toBeInTheDocument()

    const inputs = container.querySelectorAll('input[type="radio"]')
    inputs.forEach((input) => {
      expect(input).toHaveAttribute('aria-required', 'true')
    })
  })

  it('shows the question error and links it to the inputs', () => {
    const { container } = render(
      <PollChoice
        question={mandatoryQuestion}
        allowUnregisteredUsers={false}
        onAnswerChange={jest.fn()}
        errors={{ 1: ['Please answer this question to continue.'] }}
      />
    )

    const error = screen.getByRole('alert')
    expect(error).toHaveTextContent('Please answer this question to continue.')

    const input = container.querySelector('input[type="radio"]')
    expect(input).toHaveAttribute('aria-invalid', 'true')
    expect(input.getAttribute('aria-describedby')).toContain('id_error-1')
  })
})
