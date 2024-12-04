import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import { ControlBar } from '../ControlBar'
import { BrowserRouter } from 'react-router'

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

test('ControlBar shown when list is empty', () => {
  const onChangeFiltersFn = jest.fn()
  render(
    <BrowserRouter>
      <ControlBar
        filters={filters}
        onChangeFilters={() => onChangeFiltersFn()}
        numOfResults={0}
      />
    </BrowserRouter>
  )
  const numOfResultsElement = screen.queryByText(/2/)
  expect(numOfResultsElement).toBeFalsy()
  const orderingFilterElement = screen.getByText('ordering: Most recent')
  expect(orderingFilterElement).toBeTruthy()
})

test('ControlBar collapsed bar', () => {
  const onChangeFiltersFn = jest.fn()
  render(
    <BrowserRouter>
      <ControlBar
        filters={filters}
        onChangeFilters={() => onChangeFiltersFn()}
        numOfResults={2}
      />
    </BrowserRouter>
  )
  const numOfResultsElement = screen.queryByText(/2/)
  expect(numOfResultsElement).toBeFalsy()
  const orderingFilterElement = screen.getByText('ordering: Most recent')
  expect(orderingFilterElement).toBeTruthy()
})

test('ControlBar expanded bar', async () => {
  const onChangeFiltersFn = jest.fn()
  render(
    <BrowserRouter>
      <ControlBar
        filters={filters}
        onChangeFilters={() => onChangeFiltersFn()}
        numOfResults={2}
      />
    </BrowserRouter>
  )
  const filterButton = screen.getByText(/Show filters/)
  let expandedFilter = screen.queryByText(/category1/)
  expect(expandedFilter).toBeFalsy()
  fireEvent.click(filterButton)
  expandedFilter = screen.queryByText(/category1/)
  expect(expandedFilter).toBeTruthy()
})
