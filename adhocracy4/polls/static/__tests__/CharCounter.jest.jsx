// tools needed for testing
import React from 'react'
import { render } from '@testing-library/react'

// component and related data to be tested
import { CharCounter } from '../PollDetail/CharCounter'

test('<CharCounter> component renders correctly', () => {
  const tree = render(<CharCounter value="random" max={25} />)
  expect(tree).toMatchSnapshot()
})
