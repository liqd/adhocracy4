// tools needed for testing
import React from 'react'
import { render, fireEvent } from '@testing-library/react'

// component and related data to be tested
import { EditPollOpenQuestion } from '../PollDashboard/EditPollOpenQuestion.jsx'
import { QUESTION_OBJECT } from './__testdata__/QUESTION_OBJECT'

describe('<EditPollOpenQuestion> with...', () => {
  test('question textarea', () => {
    const onTextChangeFn = jest.fn()
    const tree = render(
      <EditPollOpenQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
        onLabelChange={(label) => onTextChangeFn()}
      />
    )
    const questionTextArea = tree.container.querySelector('#id_questions-1-name')
    fireEvent.change(questionTextArea, { target: { value: 'question text' } })
    expect(onTextChangeFn).toHaveBeenCalled()
  })

  test('question textarea', () => {
    const onTextChangeFn = jest.fn()
    const tree = render(
      <EditPollOpenQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
        onLabelChange={(label) => onTextChangeFn()}
      />
    )
    const questionTextArea = tree.container.querySelector('#id_questions-1-name')
    fireEvent.change(questionTextArea, { target: { value: 'question text' } })
    expect(onTextChangeFn).toHaveBeenCalled()
  })

  test('helptext button', () => {
    const tree = render(
      <EditPollOpenQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
      />
    )
    const helptextButton = tree.container.querySelector('.poll__btn--light')
    fireEvent.click(helptextButton)
  })
})
