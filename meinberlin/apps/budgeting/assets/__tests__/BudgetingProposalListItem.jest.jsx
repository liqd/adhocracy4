import React from 'react'
import { render, screen } from '@testing-library/react'
import { BudgetingProposalListItem } from '../BudgetingProposalListItem'

const permissions = {
  view_support_count: false,
  view_rate_count: true,
  view_comment_count: true
}

test('render list item with vote button', () => {
  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_feedback', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345'
  }
  render(<BudgetingProposalListItem proposal={proposal} permissions={permissions} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})

test('render list item with stats', () => {
  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    additional_item_badges_for_list_count: 0,
    item_badges_for_list: [
      ['moderator_feedback', 'wird ueberprueft', 'CONSIDERATION'],
      ['budget', '20€'], ['category', 'candalf']],
    reference_number: '2021-12345'
  }
  render(
    <BudgetingProposalListItem proposal={proposal} permissions={permissions} />
  )
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  const resolvedDate =
    screen.queryByText('created on 11. November 2021 - 2021-12345') ||
    screen.queryByText('updated on 11 November 2021 - 2021-12345')
  expect(resolvedDate).toBeTruthy()
})
