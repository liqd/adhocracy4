import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListItemStats } from './ListItemStats'

test('displaying all 3 stats', () => {
  render(
    <ListItemStats
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
