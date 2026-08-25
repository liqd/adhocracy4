import React from 'react'
import { render, screen } from '@testing-library/react'
import { PollOpenQuestion } from '../PollDetail/PollOpenQuestion'
import type { PollQuestion } from '../../../static/api/types'

describe('confidential notice when answering', () => {
  test('shown for confidential open question', () => {
    const question: PollQuestion = {
      id: 1,
      label: 'Email',
      help_text: '',
      is_confidential: true,
      isReadOnly: false,
      authenticated: true,
      userAnswer: '',
      answers: [],
      multiple_choice: false,
      is_open: true,
      image_url: null,
      image_alt_text: '',
      image_help_text: '',
      choices: [],
      userChoices: [],
      other_choice_answers: [],
      other_choice_user_answer: '',
      totalVoteCount: 0,
      totalVoteCountMulti: 0,
      totalAnswerCount: 0
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