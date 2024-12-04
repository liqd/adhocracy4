import React from 'react'
import { render, act, screen } from '@testing-library/react'
import { BudgetingProposalList } from '../BudgetingProposalList'
import { BrowserRouter } from 'react-router'

// permissions for anonymous/logged-in user during collection phase of 1 and 2 phase (3 phase is dfferent see ListItem test)
const permissions = {
  view_support_count: false,
  view_rate_count: true,
  view_comment_count: true,
  view_vote_count: false,
  has_voting_permission_and_valid_token: false
}

// permissions for anonymous/logged-in user with token during vote phase
const permissionsVote = {
  view_support_count: false,
  view_rate_count: false,
  view_comment_count: true,
  view_vote_count: false,
  has_voting_permission_and_valid_token: true
}

test('Budgeting Proposal List (1, 2, 3) - no ideas - check: empty list string', async () => {
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
  expect(screen.getByText('Nothing to show')).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})

test('Budgeting Proposal List (3) - voting, finished phase no token - all user - check: no vote count or link',
  async () => {
    // sample data (one proposal item)
    const mockedResults = [
      {
        comment_count: 6,
        created: '2021-11-11T15:36:57.941072+01:00',
        creator: 'admin',
        is_archived: false,
        name: 'erster vorschlag',
        negative_rating_count: 1,
        pk: 7,
        positive_rating_count: 3,
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
    expect(screen.getByText('erster vorschlag')).toBeTruthy()
    expect(screen.queryByText('you have 1 vote left.you have %s votes left.')).toBeNull()
    expect(screen.queryByDisplayValue('End session')).toBeNull()

    // reverse overwrite of global.fetch
    await global.fetch.mockClear()
  })

test('Budgeting Proposal List (3) - voting phase - user with token 2 votes - check: vote count + end session link',
  async () => {
    // sample data (one proposal item)
    const mockedResults = [
      {
        comment_count: 6,
        created: '2021-11-11T15:36:57.941072+01:00',
        creator: 'admin',
        is_archived: false,
        name: 'erster vorschlag',
        negative_rating_count: 1,
        pk: 7,
        positive_rating_count: 3,
        url: '/budgeting/2021-00007/',
        additional_item_badges_for_list_count: 1,
        item_badges_for_list: [
          ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
          ['budget', '20€'], ['category', 'candalf']]
      }
    ]

    // mimicking fetch response with met info for token
    const mockedFetch = Promise.resolve({
      json: () => Promise.resolve({
        results: mockedResults,
        permissions: permissionsVote,
        token_info: { num_votes_left: 2, votes_left: true }
      })
    })

    // overwrite global.fetch with mock function
    global.fetch = jest.fn().mockImplementation(() => mockedFetch)

    render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
    expect(global.fetch).toHaveBeenCalledTimes(1)

    // waiting for async fetching ends --> without this, the
    // act(...) console.error will appear
    await act(() => mockedFetch)
    expect(screen.getByText('erster vorschlag')).toBeTruthy()
    // FIXME figure out how to deal with plurals
    expect(screen.getByText('you have 1 vote left.you have %s votes left.2')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'End session' })).toBeTruthy()

    // reverse overwrite of global.fetch
    await global.fetch.mockClear()
  })

test('Budgeting Proposal List (1, 2, 3) - all users - check: fetch list item error', async () => {
  // overwrite global.fetch with mock function
  global.fetch = jest.fn().mockRejectedValue('testing: expected network error')

  render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
  expect(global.fetch).toHaveBeenCalledTimes(1)
  const emptyList = screen.queryAllByText('mock text')
  expect(emptyList).toBeTruthy()

  // reverse overwrite of global.fetch
  await global.fetch.mockClear()
})
