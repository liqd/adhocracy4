import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import { SwitchButton } from '../SwitchButton'

test('Show button correctly', () => {
  render(
    <SwitchButton
      switchLabelOff="This is the Off label"
    />
  )
  expect(screen.getByText('This is the Off label')).toBeInTheDocument()
})

test('Switch button should change state onclick', () => {
  render(
    <SwitchButton
      switchLabelOff="This is the Off label"
      switchLabelOn="This is the On label"
    />
  )
  const switchButton = screen.getByRole('switch')

  expect(switchButton).toHaveAttribute('aria-checked', 'false')
  fireEvent.click(switchButton)
  expect(switchButton).toHaveAttribute('aria-checked', 'true')
  expect(screen.getByText('This is the On label')).toBeInTheDocument()
  fireEvent.click(switchButton)
  // State should be updated back to false after the second click
  expect(switchButton).toHaveAttribute('aria-checked', 'false')
  expect(screen.getByText('This is the Off label')).toBeInTheDocument()
})
