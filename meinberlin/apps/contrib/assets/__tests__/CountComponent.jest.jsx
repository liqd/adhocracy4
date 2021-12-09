import React from 'react'
import { render, screen } from '@testing-library/react'
import { CountComponent } from '../CountComponent'

test('CountComponent is showing', () => {
  render(
    <CountComponent
      activeClass="active-class"
      inactiveClass="inactive-class"
      countText="votes"
      counter={0}
    />
  )
  const countComponent = screen.getByText('votes')
  expect(countComponent.innerHTML).toBe('votes')
})
