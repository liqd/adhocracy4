// tools needed for testing
import React from 'react'
import { render } from '@testing-library/react'

// component to be tested
import { ModeratorFeedback } from '../moderator_feedback.jsx'

test('render <ModeratorFeedback> properly', () => {
  const feedback = {
    pk: 1,
    feedbackText: 'test feedback',
    last_edit: '2020-01-01T00:00:00Z'
  }
  const tree = render(
    <ModeratorFeedback
      lastEdit={feedback.last_edit}
      feedbackText={feedback.feedbackText}
    />
  )
  expect(tree.getByText(/(test feedback)/)).toBeDefined()
})
