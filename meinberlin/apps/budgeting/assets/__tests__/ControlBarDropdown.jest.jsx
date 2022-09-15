import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { ControlBarDropdown } from '../ControlBarDropdown'

test('ControlBarDropdown is displaying with icons', () => {
  render(
    <ControlBarDropdown
      filter={{
        label: 'categories',
        current: 'all',
        icons: [['1', 'some/url']],
        choices: [['1', 'all'], ['2', 'category1']]
      }}
    />
  )
  const allChoiceElement = screen.getByText('all')
  expect(allChoiceElement).toBeTruthy()
  const iconElement = screen.getByAltText('')
  expect(iconElement).toBeTruthy()
})

test('ControlBarDropdown on filter change', () => {
  const onFilterChangeFn = jest.fn()
  render(
    <ControlBarDropdown
      filter={{
        label: 'categories',
        current: 'all',
        icons: [['1', 'some/url']],
        choices: [['1', 'all'], ['2', 'category1']]
      }}
      onSelectFilter={() => onFilterChangeFn()}
    />
  )
  const category1Element = screen.getByText(/(category1)/)
  fireEvent.click(category1Element)
  expect(onFilterChangeFn).toHaveBeenCalledTimes(1)
})

test('ControlBarDropdown is positioned right', () => {
  render(
    <ControlBarDropdown
      filter={{
        position: 'right',
        label: 'categories',
        current: 'all',
        icons: [['1', 'some/url']],
        choices: [['1', 'all'], ['2', 'category1']]
      }}
    />
  )
  const allChoiceElement = screen.getByText('all')
  expect(allChoiceElement).toBeTruthy()
})
