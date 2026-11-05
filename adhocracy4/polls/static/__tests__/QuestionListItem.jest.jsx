import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'

import { QuestionListItem } from '../PollDashboard/QuestionListItem'

const question = {
  id: 1,
  key: 'q_1',
  label: 'What is your favourite colour?',
  help_text: '',
  multiple_choice: false,
  is_open: false,
  is_confidential: false,
  choices: []
}

const defaults = {
  index: 0,
  hasErrors: false,
  isExpanded: false,
  isDragging: false,
  isDragOver: false,
  onEdit: jest.fn(),
  onDelete: jest.fn(),
  onDragStart: jest.fn(),
  onDragEnter: jest.fn(),
  onDragEnd: jest.fn(),
  onDrop: jest.fn()
}

describe('QuestionListItem', () => {
  it('renders number, label and answer type', () => {
    render(<QuestionListItem question={question} {...defaults} index={2} />)
    expect(screen.getByText('03')).toBeInTheDocument()
    expect(screen.getByText('What is your favourite colour?')).toBeInTheDocument()
    expect(screen.getByText('Single choice')).toBeInTheDocument()
  })

  it('shows placeholder for untitled questions', () => {
    render(
      <QuestionListItem
        question={{ ...question, label: '', is_open: true }}
        {...defaults}
      />
    )
    expect(screen.getByText('Untitled question')).toBeInTheDocument()
    expect(screen.getByText('Open question')).toBeInTheDocument()
  })

  it('shows multiple choice badge', () => {
    render(
      <QuestionListItem
        question={{ ...question, multiple_choice: true }}
        {...defaults}
      />
    )
    expect(screen.getByText('Multiple choice')).toBeInTheDocument()
  })

  it('opens the editor when the summary is clicked', () => {
    const onEdit = jest.fn()
    render(<QuestionListItem question={question} {...defaults} onEdit={onEdit} />)
    fireEvent.click(screen.getByText('What is your favourite colour?'))
    expect(onEdit).toHaveBeenCalledTimes(1)
  })

  it('asks for confirmation before deleting', () => {
    const onDelete = jest.fn()
    render(<QuestionListItem question={question} {...defaults} onDelete={onDelete} />)

    fireEvent.click(screen.getByLabelText('Delete question'))
    expect(onDelete).not.toHaveBeenCalled()

    fireEvent.click(screen.getByLabelText('Confirm delete'))
    expect(onDelete).toHaveBeenCalledTimes(1)
  })

  it('can cancel the delete confirmation', () => {
    const onDelete = jest.fn()
    render(<QuestionListItem question={question} {...defaults} onDelete={onDelete} />)

    fireEvent.click(screen.getByLabelText('Delete question'))
    fireEvent.click(screen.getByLabelText('Cancel delete'))
    expect(onDelete).not.toHaveBeenCalled()
    expect(screen.getByLabelText('Delete question')).toBeInTheDocument()
  })

  it('the whole row can be used to start dragging', () => {
    const { container } = render(<QuestionListItem question={question} {...defaults} />)
    const item = container.querySelector('.poll-management__item')
    expect(item).toHaveAttribute('draggable', 'true')
  })

  it('shows the collapse state on the expanded row', () => {
    const { container } = render(
      <QuestionListItem question={question} {...defaults} isExpanded />
    )
    expect(container.querySelector('.poll-management__item--active')).toBeInTheDocument()
    expect(screen.getByLabelText('Collapse question')).toBeInTheDocument()
  })

  it('marks drag over state', () => {
    const { container } = render(
      <QuestionListItem question={question} {...defaults} isDragOver />
    )
    expect(container.querySelector('.poll-management__item--drag-over')).toBeInTheDocument()
  })
})
