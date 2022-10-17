import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListItemStats } from '../ListItemStats'

test('rating displaying all 3 stats', () => {
  const permissions = {
    view_support_count: false,
    view_rate_count: true,
    view_comment_count: true
  }

  render(
    <ListItemStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
    />
  )
  const pCount = screen.getByText('4')
  expect(pCount).toBeTruthy()
  const nCount = screen.getByText('1')
  expect(nCount).toBeTruthy()
  const cCount = screen.getByText('18')
  expect(cCount).toBeTruthy()
})

test('support phase displaying 2 stats', () => {
  const permissions = {
    view_support_count: true,
    view_rate_count: false,
    view_comment_count: true
  }

  render(
    <ListItemStats
      permissions={permissions}
      positiveCount="4"
      negativeCount="1"
      commentCount="18"
    />
  )
  const pCount = screen.getByText('4')
  expect(pCount).toBeTruthy()
  const nCount = screen.queryByText('1')
  expect(nCount).toBeNull()
  const cCount = screen.getByText('18')
  expect(cCount).toBeTruthy()
})
