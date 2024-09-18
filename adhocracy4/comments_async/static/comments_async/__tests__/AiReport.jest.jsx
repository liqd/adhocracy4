import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import AiReport from '../ai_report'

describe('Test AiReport', () => {
  test('renders with Read More button', () => {
    render(
      <AiReport
        report={{ label: [['cattest', 'test label']], confidence: [['cattest', 0.65]], explanation: { cattest: [['word', 0.61]] }, show_in_discussion: true }}
      />
    )
    const comment = screen.getByText('Read more')
    expect(comment).toBeInTheDocument()
  })

  test('functionality of Read More button', () => {
    render(
      <AiReport
        report={{ label: [['cattest', 'test label']], confidence: [['cattest', 0.65]], explanation: { cattest: [['word', 0.61]] }, show_in_discussion: true }}
      />
    )
    const readMore = screen.getByText('Read more')
    expect(readMore).toBeInTheDocument()
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
    fireEvent.click(button)
    const readLess = screen.getByText('Show less')
    expect(readLess).toBeInTheDocument()
    expect(readLess).toBeInTheDocument()
  })

  test('shows percentage for each label', async () => {
    render(
      <AiReport
        report={{ label: [['cattest', 'test label']], confidence: [0.65], explanation: { cattest: [['word', 0.61]] }, show_in_discussion: true }}
      />
    )
    const readMore = screen.getByText('Read more')
    expect(readMore).toBeInTheDocument()
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
    fireEvent.click(button)
    const percent = screen.getByText(/65%/)
    expect(percent).toBeInTheDocument()
  })
})
