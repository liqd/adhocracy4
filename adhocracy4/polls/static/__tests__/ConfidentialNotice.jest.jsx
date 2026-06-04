import React from 'react'
import { render, screen } from '@testing-library/react'
import { PollOpenQuestion } from '../PollDetail/PollOpenQuestion.jsx'

describe('confidential notice when answering', () => {
  test('shown for confidential open question', () => {
    const question = {
      id: 1,
      label: 'Email',
      help_text: '',
      is_confidential: true,
      isReadOnly: false,
      authenticated: true,
      userAnswer: '',
      answers: []
    }

    render(
      <PollOpenQuestion
        question={question}
        allowUnregisteredUsers={false}
        onOpenChange={() => {}}
        errors={{}}
      />
    )

    expect(
      screen.getByText(
        'Your response will be kept confidential and will not be publicly displayed.'
      )
    ).toBeInTheDocument()
  })
})
