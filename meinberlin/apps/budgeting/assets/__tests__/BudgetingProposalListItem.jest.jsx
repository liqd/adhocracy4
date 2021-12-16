import React from 'react'
import { render, screen } from '@testing-library/react'
import { BudgetingProposalListItem } from '../BudgetingProposalListItem'
import django from '../../../../../__mocks__/djangoMock'

test('render list item with vote button', () => {
  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    moderator_feedback: ['CONSIDERATION', 'wird ueberprueft']
  }
  render(<BudgetingProposalListItem proposal={proposal} isVotingPhase />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  const resolvedDate =
    screen.queryByText(`${django.gettext()} 11. November 2021`) ||
    screen.queryByText(`${django.gettext()} 11 November 2021`)
  expect(resolvedDate).toBeTruthy()
})

test('render list item with stats', () => {
  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00',
    moderator_feedback: ['CONSIDERATION', 'wird ueberprueft']
  }
  render(
    <BudgetingProposalListItem proposal={proposal} isVotingPhase={false} />
  )
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  const resolvedDate =
    screen.queryByText(`${django.gettext()} 11. November 2021`) ||
    screen.queryByText(`${django.gettext()} 11 November 2021`)
  expect(resolvedDate).toBeTruthy()
})
