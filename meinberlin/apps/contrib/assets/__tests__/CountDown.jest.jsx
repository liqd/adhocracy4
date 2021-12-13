import React from 'react'
import { render, screen } from '@testing-library/react'
import { CountDown } from '../CountDown'

test('CountComponent is showing inactive', () => {
  render(
    <CountDown
      activeClass="active-class"
      inactiveClass="inactive-class"
      countText="votes"
      counter={0}
    />
  )
  const countComponent = screen.getByText('votes')
  expect(countComponent.innerHTML).toBe('votes')
})

test('CountComponent is showing active', () => {
  render(
    <CountDown
      activeClass="active-class"
      inactiveClass="inactive-class"
      countText="votes"
      counter={2}
    />
  )
  const countComponent = screen.getByText('votes')
  expect(countComponent.innerHTML).toBe('votes')
})
