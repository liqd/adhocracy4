import React from 'react'
import { render, fireEvent, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import AiReport from '../ai_report'

test('Test render <AiReport> with Read More button', () => {
  render(
    <AiReport
      Report={{ explanation: 'This is the ai report', show_in_discussion: true }}
    />
  )
  const comment = screen.getByText('Read more')
  expect(comment).toBeTruthy()
})

test('Test functionality of Read More <AiReport>', () => {
  render(
    <AiReport
      Report={{ explanation: 'This is the ai report', show_in_discussion: true }}
    />
  )
  const readMore = screen.getByText('Read more')
  expect(readMore).toBeTruthy()
  const button = screen.getByRole('button')
  expect(button).toBeTruthy()
  fireEvent.click(button)
  const readLess = screen.getByText('Show less')
  expect(readLess).toBeTruthy()
})
