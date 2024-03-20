import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import { ControlBarDropdown } from '../ControlBarDropdown'

describe('ControlBarDropdown', () => {
  const mockOnSelectFilter = jest.fn()

  const props = {
    onSelectFilter: mockOnSelectFilter,
    filter: {
      label: 'Test Filter',
      choices: [['choice1', 'Choice 1'], ['choice2', 'Choice 2']],
      default: 'choice1'
    },
    filterId: 'testFilter',
    current: 'choice1'
  }

  test('renders the correct default value', () => {
    render(<ControlBarDropdown {...props} />)
    expect(screen.getByLabelText('Test Filter').value).toBe('choice1')
  })

  test('calls onSelectFilter when a new option is selected', () => {
    render(<ControlBarDropdown {...props} />)
    fireEvent.change(screen.getByLabelText('Test Filter'), {
      target: { value: 'choice2' }
    })
    expect(mockOnSelectFilter).toHaveBeenCalledWith(['choice2', 'Choice 2'])
  })

  test('handles empty choices correctly', () => {
    const newProps = {
      ...props,
      filter: {
        ...props.filter,
        choices: [['', 'None'], ['choice1', 'Choice 1'], ['choice2', 'Choice 2']]
      },
      current: ''
    }
    render(<ControlBarDropdown {...newProps} />)
    expect(screen.getByLabelText('Test Filter').value).toBe('')
  })
})
