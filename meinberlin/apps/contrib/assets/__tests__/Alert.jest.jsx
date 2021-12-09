import React from 'react'
import { render, screen } from '@testing-library/react'
import Alert from '../Alert'

test('Alert is showing', () => {
  render(<Alert type="success" message="hello" />)
  const alert = screen.getByRole('alert')
  expect(alert).toBeTruthy()
})

test('Alert is not showing', () => {
  render(<Alert message="hello" />)
  const alert = screen.queryByRole('alert')
  expect(alert).toBeFalsy()
})
