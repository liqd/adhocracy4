// tools needed for testing
import React from 'react'
import { render } from '@testing-library/react'

// component to be tested
import { ModeratorStatement } from '../moderator_statement.jsx'

test('render <ModeratorStatement> properly', () => {
  const statement = {
    pk: 1,
    statement: 'test statement',
    last_edit: '2020-01-01T00:00:00Z'
  }
  const tree = render(
    <ModeratorStatement
      lastEdit={statement.last_edit}
      statement={statement.statement}
    />
  )
  expect(tree.getByText(/(test statement)/)).toBeDefined()
})
