import React from 'react'
import { render, act, screen } from '@testing-library/react'
import { BudgetingProposalList } from '../BudgetingProposalList'
import { BrowserRouter } from 'react-router-dom'

const permissions = {
  view_support_count: false,
  view_rate_count: true,
  view_comment_count: true,
  view_votes_left: true
}

test('Budgeting Proposal List without list item (empty)', async () => {
  // mimicking fetch response with empty list
  const mockedFetchEmpty = Promise.resolve({
    json: () => Promise.resolve({ results: [], permissions })
  })

  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockImplementation(() => mockedFetchEmpty)

  render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
  expect(global.fetch).toHaveBeenCalledTimes(1)

  // waiting for async fetching ends --> without this, the
  // act(...) console.error will appear
  await act(() => mockedFetchEmpty)
  const emptyList = screen.queryAllByText('mock text')
  expect(emptyList).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})

test('Budgeting Proposal List with one list item', async () => {
  // sample data (one proposal item)
  const mockedResults = [
    {
      comment_count: 0,
      created: '2021-11-11T15:36:57.941072+01:00',
      creator: 'admin',
      is_archived: false,
      name: 'erster vorschlag',
      negative_rating_count: 0,
      pk: 7,
      positive_rating_count: 0,
      url: '/budgeting/2021-00007/',
      additional_item_badges_for_list_count: 1,
      item_badges_for_list: [
        ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
        ['budget', '20€'], ['category', 'candalf']]
    }
  ]

  // mimicking fetch response
  const mockedFetch = Promise.resolve({
    json: () => Promise.resolve({ results: mockedResults, permissions })
  })

  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockImplementation(() => mockedFetch)

  render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
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

  render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
  expect(global.fetch).toHaveBeenCalledTimes(1)
  const emptyList = screen.queryAllByText('mock text')
  expect(emptyList).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})
