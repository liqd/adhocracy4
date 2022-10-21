import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListItemBadges } from '../ListItemBadges'

// testing data:
const someBadges = [
  ['category', 'category1'],
  ['label', 'label1'],
  ['label', 'label2']
]

const pointLabelBadge = [
  ['point_label', 'labelwithicon']
]

const modFeedbackBadge = [
  ['moderator_feedback', 'Under consideration', 'CONSIDERATION']
]

test('displaying 3 labels', () => {
  render(
    <ListItemBadges
      badges={someBadges}
    />
  )
  expect(screen.getByText('category1')).toBeTruthy()
  expect(screen.getByText('label1')).toBeTruthy()
  expect(screen.getByText('label2')).toBeTruthy()
})

test('displaying point label badge', () => {
  render(
    <ListItemBadges
      badges={pointLabelBadge}
    />
  )
  expect(screen.getByText('labelwithicon')).toBeTruthy()
})

test('displaying moderator feedback badge', () => {
  render(
    <ListItemBadges
      badges={modFeedbackBadge}
    />
  )
  expect(screen.getByText('Under consideration')).toBeTruthy()
})

test('displaying first 3 badges and add more link', () => {
  render(
    <ListItemBadges
      badges={someBadges}
      numOfMoreBadges={1}
    />
  )
  expect(screen.getByText('1 More')).toBeTruthy()
})
