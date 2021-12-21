import React from 'react'
import { render, screen } from '@testing-library/react'
import { FilterBar } from '../FilterBar'

const filters = {
  category: {
    label: 'categories',
    current: 'all',
    icons: [['1', 'some/url']],
    choices: [['1', 'all'], ['2', 'category1']]
  },
  ordering: {
    label: 'ordering',
    current: 'Most recent',
    choices: [['latest', 'Most recent'], ['most', 'Most voted']]
  }
}

test('FilterBar shows filters', () => {
  const onChangeFiltersFn = jest.fn()
  render(
    <FilterBar filters={filters} onChangeFilters={() => onChangeFiltersFn()} />
  )
  const categoriesFilterElement = screen.getByText('categories: all')
  expect(categoriesFilterElement).toBeTruthy()
  const orderingFilterElement = screen.getByText('ordering: Most recent')
  expect(orderingFilterElement).toBeTruthy()
})
