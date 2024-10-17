// tools needed for testing
import React from 'react'
import { render, fireEvent } from '@testing-library/react'

// component and related data to be tested
import { EditPollQuestion } from '../PollDashboard/EditPollQuestion.jsx'
import { QUESTION_OBJECT } from './__testdata__/QUESTION_OBJECT'

describe('<EditPollQuestion> with...', () => {
  test('question textarea', () => {
    const onTextChangeFn = jest.fn()
    const tree = render(
      <EditPollQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
        onLabelChange={() => onTextChangeFn()}
        // onHelptextChange={(helptext) => handleQuestion('helptext', { index, helptext })}
        // onMultipleChoiceChange={(multipleChoice) => handleQuestion('multiple-choice', { index, multipleChoice })}
        // onHasOtherChoiceChange={(isOtherChoice) => handleChoice('is-other-choice', { index, isOtherChoice })}
        // onMoveUp={index !== 0 ? () => handleQuestion('move', { index, direction: 'up' }) : null}
        // onMoveDown={index < arr.length - 1 ? () => handleQuestion('move', { index, direction: 'down' }) : null}
        // onDelete={() => handleQuestion('delete', { index })}
        // errors={errors && errors[index] ? errors[index] : {}}
        // onChoiceLabelChange={(choiceIndex, label) => handleChoice('label', { index, choiceIndex, label })}
        // onDeleteChoice={(choiceIndex) => handleChoice('delete', { index, choiceIndex })}
        // onAppendChoice={(hasOtherOption) => handleChoice('append', { index, hasOtherOption })}
      />
    )
    const questionTextArea = tree.container.querySelector('#id_questions-1-name')
    fireEvent.change(questionTextArea, { target: { value: 'question text' } })
    expect(onTextChangeFn).toHaveBeenCalled()
  })

  test('question textarea', () => {
    const onTextChangeFn = jest.fn()
    const tree = render(
      <EditPollQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
        onLabelChange={() => onTextChangeFn()}
      />
    )
    const questionTextArea = tree.container.querySelector('#id_questions-1-name')
    fireEvent.change(questionTextArea, { target: { value: 'question text' } })
    expect(onTextChangeFn).toHaveBeenCalled()
  })

  test('helptext button', () => {
    const tree = render(
      <EditPollQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
      />
    )
    const helptextButton = tree.container.querySelector('.poll__btn--light')
    fireEvent.click(helptextButton)
  })

  test('on multiple choice change', () => {
    const onMultiChoiceChangeFn = jest.fn()
    const tree = render(
      <EditPollQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
        onMultipleChoiceChange={() => onMultiChoiceChangeFn()}
      />
    )
    const multiChoiceInput = tree.container.querySelector('#id_questions-1-multiple_choice')
    fireEvent.click(multiChoiceInput)
    expect(onMultiChoiceChangeFn).toHaveBeenCalled()
  })

  test('on multiple other choice change', () => {
    const onHasOtherChoiceChangeFn = jest.fn()
    const tree = render(
      <EditPollQuestion
        id={QUESTION_OBJECT.id}
        question={QUESTION_OBJECT}
        onHasOtherChoiceChange={() => onHasOtherChoiceChangeFn()}
      />
    )
    const multiChoiceInput = tree.container.querySelector('#id_questions-1-is_other_choice')
    fireEvent.click(multiChoiceInput)
    expect(onHasOtherChoiceChangeFn).toHaveBeenCalled()
  })

  // test('on multiple other choice change', () => {
  //   const onChoiceLabelChangeFn = jest.fn()
  //   const tree = render(
  //     <EditPollQuestion
  //       id={QUESTION_OBJECT.id}
  //       question={QUESTION_OBJECT}
  //       onChoiceLabelChange={() => onChoiceLabelChangeFn()}
  //     />
  //   )
  //   const multiChoiceInput = tree.container.querySelector('#id_questions-poll-1-multiple_choice')
  //   fireEvent.click(multiChoiceInput)
  //   expect(onChoiceLabelChangeFn).toHaveBeenCalled()
  // })

  // test('on multiple other choice change', () => {
  //   const onHasOtherChoiceChangeFn = jest.fn()
  //   const tree = render(
  //     <EditPollQuestion
  //       id={QUESTION_OBJECT.id}
  //       question={QUESTION_OBJECT}
  //       onHasOtherChoiceChange={() => onHasOtherChoiceChangeFn()}
  //     />
  //   )
  //   const multiChoiceInput = tree.container.querySelector('#id_questions-poll-1-is_other_choice')
  //   fireEvent.click(multiChoiceInput)
  //   expect(onHasOtherChoiceChangeFn).toHaveBeenCalled()
  // })
})
