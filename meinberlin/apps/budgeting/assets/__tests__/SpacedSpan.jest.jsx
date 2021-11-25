import React from 'react'
import { render } from '@testing-library/react'
import { SpacedSpan } from '../SpacedSpan'

test('displaying spaced span', () => {
  const tree = render(<SpacedSpan>word</SpacedSpan>)
  // screen.debug()
  const firstSpaceSpan = tree.container.querySelector('span')
  expect(firstSpaceSpan.innerHTML).toBe(' ')
})
