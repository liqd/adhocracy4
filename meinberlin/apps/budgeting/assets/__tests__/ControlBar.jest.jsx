import React from 'react'
import { render, screen } from '@testing-library/react'
import { ControlBar } from '../ControlBar'

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

test('ControlBar shows filters', () => {
  const onChangeFiltersFn = jest.fn()
  render(
    <ControlBar
      filters={filters}
      onChangeFilters={() => onChangeFiltersFn()}
      numOfResults={2}
    />
  )
  const numOfResultsElement = screen.getByText(/2/)
  expect(numOfResultsElement).toBeTruthy()
  const orderingFilterElement = screen.getByText('ordering: Most recent')
  expect(orderingFilterElement).toBeTruthy()
})
