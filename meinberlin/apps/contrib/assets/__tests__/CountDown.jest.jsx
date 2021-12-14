import React from 'react'
import { render } from '@testing-library/react'
import { CountDown } from '../CountDown'

test('CountComponent is showing inactive', () => {
  const tree = render(
    <CountDown
      activeClass="active-class"
      inactiveClass="inactive-class"
      countText="votes"
      counter={0}
    />
  )
  const buttonInactive = tree.container.querySelector('.inactive-class')
  expect(buttonInactive).toBeTruthy()
})

test('CountComponent is showing active', () => {
  const tree = render(
    <CountDown
      activeClass="active-class"
      inactiveClass="inactive-class"
      countText="votes"
      counter={1}
    />
  )
  const buttonActive = tree.container.querySelector('.active-class')
  expect(buttonActive).toBeTruthy()
})
