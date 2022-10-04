import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListItemBadges } from '../ListItemBadges'

// testing data:
const categoryBadge = [{
  type: 'category',
  value: { id: 0, name: 'category1' }
}]

const labelsBadges = [
  {
    type: 'label',
    value: { id: 0, name: 'label1' }
  },
  {
    type: 'label',
    value: { id: 1, name: 'label2' }
  },
  {
    type: 'label',
    value: { id: 2, name: 'label3' }
  }
]

const pointLabelBadge = [{
  type: 'pointLabel',
  value: 'labelwithicon'
}]

const budgetBadge = [{
  type: 'budget',
  value: '20000'
}]

const modFeedbackBadge = [{
  type: 'modFeedback',
  value: ['CONSIDERATION', 'Under consideration']
}]

test('displaying category badge', () => {
  render(
    <ListItemBadges
      badges={categoryBadge}
    />
  )
  expect(screen.getByText('category1')).toBeTruthy()
})

test('displaying 3 labels', () => {
  render(
    <ListItemBadges
      badges={labelsBadges}
    />
  )
  expect(screen.getByText('label1')).toBeTruthy()
  expect(screen.getByText('label2')).toBeTruthy()
  expect(screen.getByText('label3')).toBeTruthy()
})

test('displaying point label badge', () => {
  render(
    <ListItemBadges
      badges={pointLabelBadge}
    />
  )
  expect(screen.getByText('labelwithicon')).toBeTruthy()
})

test('displaying budget badge with thousand separator', () => {
  render(
    <ListItemBadges
      badges={budgetBadge}
    />
  )
  expect(
    screen.queryByText('20,000€') || screen.queryByText('20.000€')
  ).toBeTruthy()
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
      badges={[...categoryBadge, ...labelsBadges]}
      numOfMoreBadges={1}
    />
  )
  expect(screen.getByText('1 More')).toBeTruthy()
})
