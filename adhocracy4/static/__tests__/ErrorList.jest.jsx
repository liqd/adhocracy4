import React from 'react'
import { render, screen } from '@testing-library/react'
import ErrorList from '../ErrorList'

test('Error is showing', () => {
  render(<ErrorList errors={{ email: ['error message'] }} field="email" />)
  const error = screen.getByText('error message', { exact: true })
  expect(error).toBeTruthy()
})

test('Error is not showing', () => {
  render(<ErrorList errors={{ email: ['error message'] }} field="name" />)
  const error = screen.queryByText('error message', { exact: true })
  expect(error).toBeFalsy()
})
