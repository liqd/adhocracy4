import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListItemStats } from '../ListItemStats'

test('2 phase: rating phase - can view comments and ratings count', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: true,
    view_comment_count: true,
    view_vote_count: false
  }

  render(
    <ListItemStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
      voteCount="7"
    />
  )
  const pCount = screen.getByText('4')
  expect(pCount).toBeTruthy()
  const nCount = screen.getByText('1')
  expect(nCount).toBeTruthy()
  const cCount = screen.getByText('18')
  expect(cCount).toBeTruthy()
  const vCount = screen.queryByText('7')
  expect(vCount).toBeNull()
})

test('3 phase: support phase - can view comments and support count', () => {
  const permissions = {
    view_support_count: true,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: false
  }

  render(
    <ListItemStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
      voteCount="7"
    />
  )
  const pCount = screen.getByText('4')
  expect(pCount).toBeTruthy()
  const nCount = screen.queryByText('1')
  expect(nCount).toBeNull()
  const cCount = screen.getByText('18')
  expect(cCount).toBeTruthy()
  const vCount = screen.queryByText('7')
  expect(vCount).toBeNull()
})

test('3 phase: finished - can view comments and vote count', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: false,
    view_comment_count: true,
    view_vote_count: true
  }

  render(
    <ListItemStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
      voteCount="7"
    />
  )
  const pCount = screen.queryByText('4')
  expect(pCount).toBeNull()
  const nCount = screen.queryByText('1')
  expect(nCount).toBeNull()
  const cCount = screen.getByText('18')
  expect(cCount).toBeTruthy()
  const vCount = screen.getByText('7')
  expect(vCount).toBeTruthy()
})
