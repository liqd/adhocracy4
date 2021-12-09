import React from 'react'
import { render, screen } from '@testing-library/react'
import CheckboxButton from '../CheckboxButton'

test('CheckboxButton is showing and is clickable', () => {
  render(
    <CheckboxButton
      onText="on text"
      offText="off text"
      onClass="on-class"
      offClass="off-class"
      uniqueID="unique-id"
    />
  )
  const checkboxButton = screen.getByText('off text')
  expect(checkboxButton.innerHTML).toBe('off text')
})
