import React from 'react'
import { render, screen } from '@testing-library/react'
import { IconSwitch } from '../IconSwitch'

test('IconSwitch is showing start state', () => {
  render(
    <IconSwitch
      activeClass="btn btn--icon btn--light switch--btn active"
      inactiveClass="btn btn--icon btn--light"
      startText="List"
      endText="Map"
      startAria="show list"
      endAria="show map"
      startIconClass="fa fa-list"
      endIconClass="fa fa-map"
      startID="show_list"
      endID="show_map"
      displayStartObject
      showStartObject={() => jest.fn()}
      showEndObject={() => jest.fn()}
    />
  )
  const startTextSpan = screen.getByText('List')
  const endTextSpan = screen.getByText('Map')
  expect(startTextSpan.innerHTML).toBe('List')
  expect(endTextSpan.innerHTML).toBe('Map')
})

test('IconSwitch is showing end state', () => {
  render(
    <IconSwitch
      activeClass="btn btn--icon btn--light switch--btn active"
      inactiveClass="btn btn--icon btn--light"
      startText="List"
      endText="Map"
      startAria="show list"
      endAria="show map"
      startIconClass="fa fa-list"
      endIconClass="fa fa-map"
      startID="show_list"
      endID="show_map"
      displayStartObject={false}
      showStartObject={() => jest.fn()}
      showEndObject={() => jest.fn()}
    />
  )
  const startTextSpan = screen.getByText('List')
  const endTextSpan = screen.getByText('Map')
  expect(startTextSpan.innerHTML).toBe('List')
  expect(endTextSpan.innerHTML).toBe('Map')
})
