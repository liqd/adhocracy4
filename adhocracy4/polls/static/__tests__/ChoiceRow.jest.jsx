import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { ChoiceRow } from '../PollDetail/ChoiceRow'

// Mock of the TextareaWithCounter component
jest.mock('../PollDetail/TextareaWithCounter', () => ({
  TextareaWithCounter: ({ value, onChange }) => (
    <textarea value={value} onChange={onChange} data-testid="textarea-with-counter-2" />
  )
}))

describe('ChoiceRow', () => {
  const mockOnInputChange = jest.fn()
  const mockOnOtherChange = jest.fn()

  const defaultProps = {
    choice: {
      id: 1,
      label: 'Option 1',
      is_other_choice: false
    },
    checked: false,
    onInputChange: mockOnInputChange,
    type: 'radio',
    disabled: false,
    otherChoiceAnswer: '',
    onOtherChange: mockOnOtherChange,
    isAuthenticated: true,
    isReadOnly: false,
    errors: null
  }

  it('should render the ChoiceRow correctly', () => {
    render(<ChoiceRow {...defaultProps} />)

    // Check if the label and input are rendered
    expect(screen.getByText('Option 1')).toBeInTheDocument()
    expect(screen.getByRole('radio')).toBeInTheDocument()
  })

  it('should show textarea when "Other" option is selected', () => {
    const otherChoiceProps = {
      ...defaultProps,
      choice: {
        id: 2,
        label: 'Other',
        is_other_choice: true
      }
    }

    render(<ChoiceRow {...otherChoiceProps} />)

    // Initially, textarea should not be visible
    expect(screen.queryByTestId('textarea-with-counter-2')).toBeNull()

    // Simulate selecting the "Other" radio button
    fireEvent.click(screen.getByRole('radio'))

    // Textarea should now be visible
    expect(screen.getByTestId('textarea-with-counter-2')).toBeInTheDocument()
  })

  it('should update textarea value on change', () => {
    const otherChoiceProps = {
      ...defaultProps,
      choice: {
        id: 2,
        label: 'Other',
        is_other_choice: true
      }
    }

    render(<ChoiceRow {...otherChoiceProps} />)

    fireEvent.click(screen.getByRole('radio')) // Selecting the "Other" option

    // Get the textarea and simulate typing
    const textarea = screen.getByTestId('textarea-with-counter-2')
    fireEvent.change(textarea, { target: { value: 'New answer' } })

    // Check that the textarea value was updated
    expect(textarea.value).toBe('New answer')
    expect(mockOnOtherChange).toHaveBeenCalledWith(expect.anything()) // Check if the onOtherChange function was called
  })

  it('should not show textarea when "Other" option is not selected', () => {
    render(<ChoiceRow {...defaultProps} />)

    // Check if the textarea is not shown when the "Other" option is not selected
    expect(screen.queryByTestId('textarea')).toBeNull()
  })
})
