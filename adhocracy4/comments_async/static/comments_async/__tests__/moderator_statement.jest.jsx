// tools needed for testing
import React from 'react'
import { render } from '@testing-library/react'

// component to be tested
import { ModeratorStatement } from '../moderator_statement.jsx'

test('render <ModeratorStatement> properly', () => {
  const statement = {
    pk: 1,
    statement: 'test statement',
    last_edited: '2020-01-01T00:00:00Z'
  }
  const tree = render(
    <ModeratorStatement {...statement} />
  )
  expect(tree.getByText(/(test statement)/)).toBeDefined()
})
