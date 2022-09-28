import React from 'react'
import { render, screen } from '@testing-library/react'
import { ControlBarSearchTerm } from '../ControlBarSearchTerm'

test('ControlBarSearchTerm showing searchterm', () => {
  render(
    <ControlBarSearchTerm
      term="example"
    />
  )
  const termbutton = screen.getByText('example')
  expect(termbutton).toBeTruthy()
})
