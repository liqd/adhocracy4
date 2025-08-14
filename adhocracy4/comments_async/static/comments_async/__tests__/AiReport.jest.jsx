import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import { describe, test, expect } from 'vitest' // Import from vitest

import AiReport from '../ai_report'

describe('Test AiReport', () => {
  const testReport = {
    label: [['cattest', 'test label']],
    confidence: [['cattest', 0.65]],
    explanation: { cattest: [['word', 0.61]] },
    show_in_discussion: true
  }

  test('renders with Read More button', () => {
    render(<AiReport report={testReport} />)
    expect(screen.getByText('Read more')).toBeInTheDocument()
  })

  test('functionality of Read More button', async () => {
    render(<AiReport report={testReport} />)
    const button = screen.getByRole('button')
    fireEvent.click(button)
    const showLessButton = screen.getByText('Show less')
    await expect(showLessButton).toHaveTextContent('Show less')
  })

  test('shows percentage for each label', () => {
    render(<AiReport report={{ ...testReport, confidence: [0.65] }} />)
    const button = screen.getByRole('button')
    fireEvent.click(button)
    expect(screen.getByText(/65%/)).toBeInTheDocument()
  })
})
