import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

jest.mock('django', () => ({
  gettext: (text) => text,
  pgettext: (context, text) => text,
  ngettext: (number, text) => text + number,
  interpolate: (fmt, data, named) => {
    if (named) {
      return fmt.replace(/%\((\w+)\)s/g, (match, key) => data[key])
    }
    return fmt
  }
}))

import { QuestionEditor } from '../PollDashboard/QuestionEditor'

const question = {
  id: 1,
  key: 'q_1',
  label: 'First question',
  help_text: '',
  multiple_choice: false,
  is_open: false,
  is_confidential: false,
  choices: [
    { id: 10, key: 'c_10', label: 'A', is_other_choice: false },
    { id: 11, key: 'c_11', label: 'B', is_other_choice: false }
  ]
}

const defaults = {
  index: 0,
  total: 3,
  errors: {},
  questionImagesEnabled: false,
  onLabelChange: jest.fn(),
  onHelpTextChange: jest.fn(),
  onConfidentialChange: jest.fn(),
  onMultipleChoiceChange: jest.fn(),
  onOpenChange: jest.fn(),
  onImageChange: jest.fn(),
  onAltTextChange: jest.fn(),
  onChoiceLabelChange: jest.fn(),
  onChoiceDelete: jest.fn(),
  onChoiceAppend: jest.fn(),
  onOtherChoiceToggle: jest.fn(),
  onMove: jest.fn()
}

describe('QuestionEditor', () => {
  it('shows the position within the poll without the word "Question"', () => {
    render(<QuestionEditor question={question} {...defaults} index={1} />)
    expect(screen.getByText('2 of 3')).toBeInTheDocument()
    expect(screen.queryByText('Question 2 of 3')).not.toBeInTheDocument()
  })

  it('does not render save and cancel buttons', () => {
    render(<QuestionEditor question={question} {...defaults} />)
    expect(screen.queryByText('Save')).not.toBeInTheDocument()
    expect(screen.queryByText('Cancel')).not.toBeInTheDocument()
  })

  it('disables move up on first and move down on last question', () => {
    const { rerender } = render(<QuestionEditor question={question} {...defaults} index={0} total={2} />)
    expect(screen.getByLabelText('Move question up')).toBeDisabled()
    expect(screen.getByLabelText('Move question down')).not.toBeDisabled()

    rerender(<QuestionEditor question={question} {...defaults} index={1} total={2} />)
    expect(screen.getByLabelText('Move question up')).not.toBeDisabled()
    expect(screen.getByLabelText('Move question down')).toBeDisabled()
  })

  it('moves the question up and down', () => {
    const onMove = jest.fn()
    render(<QuestionEditor question={question} {...defaults} index={1} total={3} onMove={onMove} />)
    fireEvent.click(screen.getByLabelText('Move question up'))
    expect(onMove).toHaveBeenLastCalledWith(-1)
    fireEvent.click(screen.getByLabelText('Move question down'))
    expect(onMove).toHaveBeenLastCalledWith(1)
  })

  it('changes the answer type via the segmented control', () => {
    const onMultipleChoiceChange = jest.fn()
    const onOpenChange = jest.fn()
    render(
      <QuestionEditor
        question={question}
        {...defaults}
        onMultipleChoiceChange={onMultipleChoiceChange}
        onOpenChange={onOpenChange}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Multiple choice' }))
    expect(onOpenChange).toHaveBeenCalledWith(false)
    expect(onMultipleChoiceChange).toHaveBeenCalledWith(true)

    fireEvent.click(screen.getByRole('button', { name: 'Single choice' }))
    expect(onMultipleChoiceChange).toHaveBeenCalledWith(false)

    fireEvent.click(screen.getByRole('button', { name: 'Open Text' }))
    expect(onOpenChange).toHaveBeenCalledWith(true)
  })

  it('adds and toggles answer options for multiple choice', () => {
    const onChoiceAppend = jest.fn()
    const onOtherChoiceToggle = jest.fn()
    render(
      <QuestionEditor
        question={{ ...question, multiple_choice: true }}
        {...defaults}
        onChoiceAppend={onChoiceAppend}
        onOtherChoiceToggle={onOtherChoiceToggle}
      />
    )
    fireEvent.click(screen.getByText('Answer option'))
    expect(onChoiceAppend).toHaveBeenCalledTimes(1)
    fireEvent.click(screen.getByText('Open answer'))
    expect(onOtherChoiceToggle).toHaveBeenCalledTimes(1)
  })

  it('shows all answers and allows adding answers for single choice', () => {
    render(<QuestionEditor question={question} {...defaults} />)
    expect(screen.getAllByText(/^Answer #/)).toHaveLength(2)
    expect(screen.getByText('Answer #1')).toBeInTheDocument()
    expect(screen.getByText('Answer #2')).toBeInTheDocument()
    expect(screen.getByText('Answer option')).toBeInTheDocument()
  })

  it('keeps the other (open) answer for single choice', () => {
    render(
      <QuestionEditor
        question={{
          ...question,
          choices: [...question.choices, { id: 12, key: 'c_12', label: 'other', is_other_choice: true }]
        }}
        {...defaults}
      />
    )
    expect(screen.getAllByText(/^Answer #/)).toHaveLength(2)
    expect(screen.getByLabelText('Other')).toBeInTheDocument()
    expect(screen.getByText('Answer option')).toBeInTheDocument()
  })

  it('renders the other answer option as disabled input', () => {
    render(
      <QuestionEditor
        question={{
          ...question,
          choices: [...question.choices, { id: 12, key: 'c_12', label: 'other', is_other_choice: true }]
        }}
        {...defaults}
      />
    )
    const otherInput = screen.getByLabelText('Other')
    expect(otherInput).toBeDisabled()
  })

  it('toggles the explanation field', () => {
    render(<QuestionEditor question={question} {...defaults} />)
    expect(screen.queryByRole('textbox', { name: 'Explanation' })).not.toBeInTheDocument()
    fireEvent.click(screen.getByText('Explanation'))
    expect(screen.getByRole('textbox', { name: 'Explanation' })).toBeInTheDocument()
  })

  it('shows explanation when the question already has one', () => {
    render(
      <QuestionEditor question={{ ...question, help_text: 'because' }} {...defaults} />
    )
    expect(screen.getByRole('textbox', { name: 'Explanation' })).toHaveValue('because')
  })

  it('hides answer options but keeps the answer type for open questions', () => {
    render(
      <QuestionEditor question={{ ...question, is_open: true, choices: [] }} {...defaults} />
    )
    expect(screen.queryByText('Answer option')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Open Text' })).toHaveAttribute('aria-pressed', 'true')
    expect(screen.getByRole('button', { name: 'Multiple choice' })).toHaveAttribute('aria-pressed', 'false')
    expect(screen.getByText('Explanation')).toBeInTheDocument()
  })
})
