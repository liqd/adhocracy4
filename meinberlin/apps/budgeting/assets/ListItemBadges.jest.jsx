import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListItemBadges } from './ListItemBadges'

test('displaying category badge', () => {
  render(<ListItemBadges category={{ name: 'Renovation' }} />)
  expect(screen.getByText('Renovation')).toBeTruthy()
})

test('displaying point label badge', () => {
  render(<ListItemBadges pointLabel="Bezirk Ost" />)
  expect(screen.getByText('Bezirk Ost')).toBeTruthy()
})

test('displaying budget badge with thousand separator', () => {
  render(<ListItemBadges budget="20000" />)
  expect(screen.queryByText('20,000€') || screen.queryByText('20.000€'))
    .toBeTruthy()
})

test('displaying moderator feedback badge', () => {
  render(
    <ListItemBadges
      moderatorFeedback="CONSIDERATION"
      moderatorChoices={[['CONSIDERATION', 'wird ueberprueft']]}
    />
  )
  expect(screen.getByText('wird ueberprueft')).toBeTruthy()
})
