import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, test, expect, vi } from 'vitest'
import { EditPollQuestion } from '../PollDashboard/EditPollQuestion'
import { QUESTION_OBJECT } from './__testdata__/QUESTION_OBJECT.js'

vi.mock('react-flip-move', () => {
  const MockFlipMove = ({ children }: { children: React.ReactNode }) => (
    <div data-testid="flip-move">{children}</div>
  )

  return {
    __esModule: true,
    default: MockFlipMove
  }
})

describe('<EditPollQuestion>', () => {
  // Test data
  const defaultProps = {
    id: QUESTION_OBJECT.id,
    question: QUESTION_OBJECT,
    onLabelChange: vi.fn(),
    onHelptextChange: vi.fn(),
    onMultipleChoiceChange: vi.fn(),
    onHasOtherChoiceChange: vi.fn(),
    onChoiceLabelChange: vi.fn(),
    onDeleteChoice: vi.fn(),
    onAppendChoice: vi.fn(),
    onMoveUp: vi.fn(),
    onMoveDown: vi.fn(),
    onDelete: vi.fn()
  }

  // Helper function to render the component with custom props
  const renderComponent = (overrideProps = {}) => {
    const props = { ...defaultProps, ...overrideProps }
    return render(<EditPollQuestion {...props} />)
  }

  test('renders question textarea and handles changes', () => {
    console.log('EditPollQuestion component:', EditPollQuestion)
    renderComponent()
    const textarea = screen.getByLabelText(/question/i)
    fireEvent.change(textarea, { target: { value: 'Updated question' } })
    expect(defaultProps.onLabelChange).toHaveBeenCalledWith('Updated question')
  })

  test.skip('toggles helptext section when button is clicked', () => {
    renderComponent()
    const helptextButton = screen.getByRole('button', { name: /explanation/i })
    fireEvent.click(helptextButton)
    expect(screen.getByText('Helptext Form')).toBeInTheDocument()
  })

  test('handles multiple choice toggle', () => {
    renderComponent()
    const checkbox = screen.getByRole('checkbox', { name: /multiple choice/i })
    fireEvent.click(checkbox)
    expect(defaultProps.onMultipleChoiceChange).toHaveBeenCalledTimes(1)
  })

  test('handles other choice option toggle', () => {
    renderComponent()
    const checkbox = screen.getByRole('checkbox', { name: /add their own answer/i })
    fireEvent.click(checkbox)
    expect(defaultProps.onHasOtherChoiceChange).toHaveBeenCalledTimes(1)
  })

  test('displays error messages when present', () => {
    const errors = {
      label: 'Question text is required',
      choices: ['Choice 1 is invalid']
    }
    renderComponent({ errors })
    expect(screen.getByText('Question text is required')).toBeInTheDocument()
  })

  test('handles choice label changes', () => {
    renderComponent()
    const choiceInputs = screen.getAllByLabelText(/answer #/i)
    fireEvent.change(choiceInputs[0], { target: { value: 'Updated choice' } })
    expect(defaultProps.onChoiceLabelChange).toHaveBeenCalledWith(0, 'Updated choice')
  })

  test('renders action buttons', () => {
    renderComponent()
    expect(screen.getByRole('button', { name: /new answer/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /move up/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /move down/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument()
  })

  test('disables move buttons when appropriate', () => {
    renderComponent({
      onMoveUp: undefined,
      onMoveDown: undefined
    })
    expect(screen.getByRole('button', { name: /move up/i })).toBeDisabled()
    expect(screen.getByRole('button', { name: /move down/i })).toBeDisabled()
  })
})
