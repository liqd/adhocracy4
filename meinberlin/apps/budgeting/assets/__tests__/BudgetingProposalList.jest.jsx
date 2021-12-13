import React from 'react'
import { render, act, screen } from '@testing-library/react'
import { BudgetingProposalList } from '../BudgetingProposalList'

test('Budgeting Proposal List without list item (empty)', async () => {
  // mimicking fetch response with empty list
  const mockedFetchEmpty = Promise.resolve({
    json: () => Promise.resolve({ results: [] })
  })

  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockImplementation(() => mockedFetchEmpty)

  render(<BudgetingProposalList />)
  expect(global.fetch).toHaveBeenCalledTimes(1)

  // waiting for async fetching ends --> without this, the
  // act(...) console.error will appear
  await act(() => mockedFetchEmpty)
  const emptyList = screen.queryByText('mock text')
  expect(emptyList).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})

test('Budgeting Proposal List with one list item', async () => {
  // sample data (one proposal item)
  const mockedResults = [
    {
      budget: 0,
      category: { id: 3, name: 'candalf' },
      comment_count: 0,
      created: '2021-11-11T15:36:57.941072+01:00',
      creator: 'admin',
      is_archived: false,
      locale: 'de-DE',
      moderator_feedback: null,
      moderator_feedback_choices: [],
      name: 'erster vorschlag',
      negative_rating_count: 0,
      pk: 7,
      positive_rating_count: 0,
      url: '/budgeting/2021-00007/'
    }
  ]

  // mimicking fetch response
  const mockedFetch = Promise.resolve({
    json: () => Promise.resolve({ results: mockedResults })
  })

  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockImplementation(() => mockedFetch)

  render(<BudgetingProposalList />)
  expect(global.fetch).toHaveBeenCalledTimes(1)

  // waiting for async fetching ends --> without this, the
  // act(...) console.error will appear
  await act(() => mockedFetch)
  const listItem = screen.queryByText('erster vorschlag')
  expect(listItem).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})

test('Budgeting Proposal List with fetch error', async () => {
  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockRejectedValue('testing: expected network error')

  render(<BudgetingProposalList />)
  expect(global.fetch).toHaveBeenCalledTimes(1)
  const emptyList = screen.queryByText('mock text')
  expect(emptyList).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})
