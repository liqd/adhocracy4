import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

import { ChoiceRow } from '../PollDetail/ChoiceRow'

describe('ChoiceRow', () => {
  const baseChoice = { id: 1, label: 'Option A', is_other_choice: false }
  const otherChoice = { id: 2, label: 'other', is_other_choice: true }

  it('renders the label', () => {
    render(
      <ChoiceRow
        choice={baseChoice} checked={false} type="radio"
        onInputChange={jest.fn()} onOtherChange={jest.fn()}
      />
    )
    expect(screen.getByText('Option A')).toBeInTheDocument()
  })

  it('shows the checked state', () => {
    const { container } = render(
      <ChoiceRow
        choice={baseChoice} checked type="radio"
        onInputChange={jest.fn()} onOtherChange={jest.fn()}
      />
    )
    expect(container.querySelector('input[type="radio"]')).toBeChecked()
  })

  it('shows a textarea for the other choice when checked', () => {
    render(
      <ChoiceRow
        choice={otherChoice} checked type="radio"
        onInputChange={jest.fn()} onOtherChange={jest.fn()} otherChoiceAnswer=""
      />
    )
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('hides the textarea for the other choice when unchecked', () => {
    render(
      <ChoiceRow
        choice={otherChoice} checked={false} type="radio"
        onInputChange={jest.fn()} onOtherChange={jest.fn()}
      />
    )
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument()
  })

  it('adds the review modifier class', () => {
    const { container } = render(
      <ChoiceRow
        choice={baseChoice} checked={false} type="radio" isResult review
        onInputChange={jest.fn()} onOtherChange={jest.fn()}
      />
    )
    expect(container.querySelector('label')).toHaveClass('poll-choice--review')
  })

  it('calls onOtherChange on textarea input', () => {
    const onOtherChange = jest.fn()
    render(
      <ChoiceRow
        choice={otherChoice} checked type="radio"
        onInputChange={jest.fn()} onOtherChange={onOtherChange} otherChoiceAnswer=""
      />
    )
    fireEvent.change(screen.getByRole('textbox'), { target: { value: 'x' } })
    expect(onOtherChange).toHaveBeenCalledTimes(1)
  })
})
