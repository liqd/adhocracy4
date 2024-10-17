// tools needed for testing
import React from 'react'
import { render, fireEvent } from '@testing-library/react'

// component and related data to be tested
import { PollQuestion } from '../PollDetail/PollQuestion.jsx'
import { QUESTION_OBJECT } from './__testdata__/QUESTION_OBJECT'

describe('render <PollQuestion> with...', () => {
  test('-> single-choice -> non-open-asnwers', () => {
    const tree = render(<PollQuestion question={QUESTION_OBJECT} />)
    expect(tree).toMatchSnapshot()
  })

  test('-> single-choice -> open-asnwers', () => {
    const singleOpenQuestion = { ...QUESTION_OBJECT }
    singleOpenQuestion.is_open = true
    const tree = render(<PollQuestion question={singleOpenQuestion} />)
    expect(tree).toMatchSnapshot()
  })

  test('-> multiple-choice -> non-open-asnwers', () => {
    const multiQuestion = { ...QUESTION_OBJECT }
    multiQuestion.multiple_choice = true
    const tree = render(<PollQuestion question={multiQuestion} />)
    expect(tree).toMatchSnapshot()
  })

  test('-> multiple-choice -> open-asnwers', () => {
    const multiOpenQuestion = { ...QUESTION_OBJECT }
    multiOpenQuestion.multiple_choice = true
    multiOpenQuestion.is_open = true
    const tree = render(<PollQuestion question={multiOpenQuestion} />)
    expect(tree).toMatchSnapshot()
  })
})

describe('calling prop-passed functions...', () => {
  const changedFn = jest.fn()
  const otherChangedFn = jest.fn()
  const multiChangedFn = jest.fn()

  test('call onSingleChange', () => {
    const tree = render(
      <PollQuestion
        question={QUESTION_OBJECT}
        onSingleChange={changedFn}
        onOtherChange={otherChangedFn}
      />
    )
    const choiceRadio1 = tree.container.querySelector('#id_choice-1-single')
    expect(choiceRadio1.checked).toBe(false)
    fireEvent.click(choiceRadio1)
    expect(changedFn).toHaveBeenCalled()
    expect(otherChangedFn).toHaveBeenCalled()
  })

  test('call onSingleChange -> is_other_choice', () => {
    const singleOpenQuestion = { ...QUESTION_OBJECT }
    singleOpenQuestion.choices[0].is_other_choice = true
    const tree = render(
      <PollQuestion
        question={singleOpenQuestion}
        onSingleChange={changedFn}
        onOtherChange={otherChangedFn}
      />
    )
    const choiceRadio = tree.container.querySelector('#id_choice-1-other')
    const choiceTextInput = tree.container.querySelector('#id_choice-1-other')
    expect(choiceRadio.checked).toBe(false)
    expect(choiceTextInput.value).toBe('')
    fireEvent.click(choiceRadio)
    fireEvent.change(choiceTextInput, { target: { value: 'something' } })
    expect(otherChangedFn).toHaveBeenCalled()
    expect(otherChangedFn).toHaveBeenCalledWith(1, 'something')
  })

  test('call onMultiChange', () => {
    const multiQuestion = { ...QUESTION_OBJECT }
    multiQuestion.multiple_choice = true
    multiQuestion.choices[0].is_other_choice = false
    const tree = render(
      <PollQuestion
        question={multiQuestion}
        onMultiChange={multiChangedFn}
        onOtherChange={otherChangedFn}
      />
    )
    const choiceCheckbox1 = tree.container.querySelector('#id_choice-1-multiple')
    expect(choiceCheckbox1.checked).toBe(false)
    fireEvent.click(choiceCheckbox1)
    expect(multiChangedFn).toHaveBeenCalled()
    expect(otherChangedFn).toHaveBeenCalled()
  })

  test('call onMultiChange -> is_other_choice', () => {
    const multiOpenQuestion = { ...QUESTION_OBJECT }
    multiOpenQuestion.multiple_choice = true
    multiOpenQuestion.choices[0].is_other_choice = true
    const tree = render(
      <PollQuestion
        question={multiOpenQuestion}
        onMultiChange={multiChangedFn}
        onOtherChange={otherChangedFn}
      />
    )
    const choiceCheckbox = tree.container.querySelector('#id_choice-1-multiple')
    const choiceTextInput = tree.container.querySelector('#id_choice-1-other')
    expect(choiceCheckbox.checked).toBe(false)
    expect(choiceTextInput.value).toBe('')
    fireEvent.click(choiceCheckbox)
    fireEvent.change(choiceTextInput, { target: { value: 'something' } })
    expect(otherChangedFn).toHaveBeenCalled()
    expect(otherChangedFn).toHaveBeenCalledWith(1, 'something')
  })
})

test('initialize with function getUserAnswer -> with user answer', () => {
  const userAnswerQuestion = { ...QUESTION_OBJECT }
  userAnswerQuestion.other_choice_answers = [{ answer: 'antwoord', vote_id: 1 }]
  userAnswerQuestion.other_choice_user_answer = 1

  const tree = render(
    <PollQuestion
      question={userAnswerQuestion}
    />
  )
  const choiceTextInput = tree.container.querySelector('#id_choice-1-other')
  expect(choiceTextInput.value).toBe('antwoord')
})
