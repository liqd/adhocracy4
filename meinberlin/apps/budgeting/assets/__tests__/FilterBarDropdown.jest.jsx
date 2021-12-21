import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { FilterBarDropdown } from '../FilterBarDropdown'

test('FilterBarDropdown is displaying with icons', () => {
  render(
    <FilterBarDropdown
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

test('FilterBarDropdown on filter change', () => {
  const onFilterChangeFn = jest.fn()
  render(
    <FilterBarDropdown
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

test('FilterBarDropdown is positioned right', () => {
  render(
    <FilterBarDropdown
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
