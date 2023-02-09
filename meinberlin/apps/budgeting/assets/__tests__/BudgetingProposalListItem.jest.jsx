import React from 'react'
import { render, screen } from '@testing-library/react'
import { BudgetingProposalListItem } from '../BudgetingProposalListItem'

test('Budgeting Proposal ListItem (1,2) - collection phase - initiator, mod, logged-in, anonymous users (admin sees all stats in all phases)', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: true,
    view_comment_count: true,
    vote_allowed: false,
    has_voting_permission_and_valid_token: false
  }

  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345',
    positive_rating_count: 2,
    negative_rating_count: 1,
    support_count: 8,
    vote_count: 1,
    comment_count: 7,
    pk: 7,
    vote_allowed: false
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  // support string renders multiple strings due to plurals so using title
  expect(screen.queryByTitle('Support')).toBeNull()
  expect(screen.queryByText('Total votes')).toBeNull()
  expect(screen.getByText('Comments')).toBeTruthy()
  expect(screen.getByText('Positive Ratings')).toBeTruthy()
  expect(screen.getByText('Negative Ratings')).toBeTruthy()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})

test('Budgeting Proposal ListItem (3) - collection phase - initiator, mod, logged-in, anonymous users', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: false,
    view_comment_count: true,
    vote_allowed: false,
    has_voting_permission_and_valid_token: false
  }

  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345',
    positive_rating_count: 2,
    negative_rating_count: 1,
    support_count: 8,
    vote_count: 1,
    comment_count: 7,
    pk: 7,
    vote_allowed: false
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.queryByTitle('Support')).toBeNull()
  expect(screen.queryByText('Total votes')).toBeNull()
  expect(screen.getByText('Comments')).toBeTruthy()
  expect(screen.queryByText('Positive Ratings')).toBeNull()
  expect(screen.queryByText('Negative Ratings')).toBeNull()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})

test('Budgeting Proposal ListItem (3) - support phase and between support and vote phase - initiator, mod, logged-in, anonymous users', () => {
  const permissions = {
    view_support_count: true,
    view_rate_count: false,
    view_comment_count: true,
    vote_allowed: false,
    has_voting_permission_and_valid_token: false
  }

  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345',
    positive_rating_count: 2,
    negative_rating_count: 1,
    support_count: 8,
    vote_count: 1,
    comment_count: 7,
    pk: 7,
    vote_allowed: false
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.getByTitle('Support')).toBeTruthy()
  expect(screen.queryByText('Total votes')).toBeNull()
  expect(screen.getByText('Comments')).toBeTruthy()
  expect(screen.queryByText('Positive Ratings')).toBeNull()
  expect(screen.queryByText('Negative Ratings')).toBeNull()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})

test('Budgeting Proposal ListItem (3) - vote phase with token - logged-in, anonymous', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: false,
    vote_allowed: true,
    has_voting_permission_and_valid_token: true
  }

  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345',
    positive_rating_count: 2,
    negative_rating_count: 1,
    support_count: 8,
    vote_count: 1,
    comment_count: 7,
    pk: 7,
    vote_allowed: true
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.queryByTitle('Support')).toBeNull()
  expect(screen.queryByText('Total votes')).toBeNull()
  expect(screen.getByText('Comments')).toBeTruthy()
  expect(screen.queryByText('Positive Ratings')).toBeNull()
  expect(screen.queryByText('Negative Ratings')).toBeNull()
  expect(screen.getByText('Give my vote')).toBeTruthy()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})

test('Budgeting Proposal ListItem (3) - vote phase with token - initiator, moderator', () => {
  const permissions = {
    view_support_count: true,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: false,
    vote_allowed: true,
    has_voting_permission_and_valid_token: true
  }

  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345',
    positive_rating_count: 2,
    negative_rating_count: 1,
    support_count: 8,
    vote_count: 1,
    comment_count: 7,
    pk: 7,
    vote_allowed: true
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.getByTitle('Support')).toBeTruthy()
  expect(screen.queryByText('Total votes')).toBeNull()
  expect(screen.getByText('Comments')).toBeTruthy()
  expect(screen.queryByText('Positive Ratings')).toBeNull()
  expect(screen.queryByText('Negative Ratings')).toBeNull()
  expect(screen.getByText('Give my vote')).toBeTruthy()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})

test('Budgeting Proposal ListItem (3) - finished - logged-in, anonymous', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: true,
    vote_allowed: false,
    has_voting_permission_and_valid_token: false
  }

  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345',
    positive_rating_count: 2,
    negative_rating_count: 1,
    support_count: 8,
    vote_count: 1,
    comment_count: 7,
    pk: 7,
    vote_allowed: true
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.queryByTitle('Support')).toBeNull()
  expect(screen.getByText('Total votes')).toBeTruthy()
  expect(screen.getByText('Comments')).toBeTruthy()
  expect(screen.queryByText('Positive Ratings')).toBeNull()
  expect(screen.queryByText('Negative Ratings')).toBeNull()
  expect(screen.queryByText('Give my vote')).toBeNull()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})
