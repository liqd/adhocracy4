import React, { useEffect, useState } from 'react'
import django from 'django'
import { ChoiceRow } from './ChoiceRow'
import { PollQuestionLayout } from './PollQuestionLayout'
const translated = {
  multiple: django.gettext('Multiple answers are possible.')
}

export const PollChoice = ({
  question,
  allowUnregisteredUsers,
  onSingleChange,
  onMultiChange,
  onOtherChange,
  errors,
  questionImagesEnabled
}) => {
  const getUserAnswer = () => {
    const userAnswerId = question.other_choice_user_answer
    const userAnswer = question.other_choice_answers.find(oc => oc.vote_id === userAnswerId)
    return question.other_choice_answer
      ? question.other_choice_answer
      : ((userAnswerId && userAnswer)
          ? userAnswer.answer
          : ''
        )
  }

  const [userChoices, setUserChoices] = useState([])
  const [otherChoiceAnswer, setOtherChoiceAnswer] = useState(getUserAnswer())

  const multiHelpText = question.multiple_choice ? <div className="poll__help-text">{translated.multiple}</div> : null
  const userAllowedVote = question.authenticated || allowUnregisteredUsers

  useEffect(() => {
    setUserChoices(question.userChoices || [])
  }, [question.userChoices])

  const findOtherChoice = () => {
    return question.choices.find(c => c.is_other_choice)
  }

  const handleSingleChange = (event, isOther) => {
    const choiceId = parseInt(event.target.value)
    setUserChoices([choiceId])
    onSingleChange(question.id, choiceId)
    if (!isOther) {
      setOtherChoiceAnswer('')
      onOtherChange(question.id, '', findOtherChoice())
    }
  }

  const handleMultiChange = (event, isOther) => {
    const choiceId = parseInt(event.target.value)
    const newChoices = userChoices.includes(choiceId)
      ? userChoices.filter(id => id !== choiceId)
      : [...userChoices, choiceId]

    setUserChoices(newChoices)
    onMultiChange(question.id, choiceId)

    if (!newChoices.includes(findOtherChoice()?.id)) {
      setOtherChoiceAnswer('')
      onOtherChange(question.id, '', findOtherChoice())
    }
  }

  const handleOtherChange = (event) => {
    const otherAnswer = event.target.value
    setOtherChoiceAnswer(otherAnswer)
    onOtherChange(question.id, otherAnswer)
  }

  return (
    <PollQuestionLayout question={question} questionImagesEnabled={questionImagesEnabled}>
      {multiHelpText}
      <div className="poll__rows">
        {question.choices.map((choice) => {
          const checked = userChoices.indexOf(choice.id) !== -1
          return (
            <ChoiceRow
              key={choice.id}
              choice={choice}
              checked={checked}
              onInputChange={question.multiple_choice ? handleMultiChange : handleSingleChange}
              type={question.multiple_choice ? 'checkbox' : 'radio'}
              disabled={!userAllowedVote || question.isReadOnly}
              otherChoiceAnswer={otherChoiceAnswer}
              onOtherChange={handleOtherChange}
              isReadOnly={question.isReadOnly}
              errors={errors}
              name={question.multiple_choice ? undefined : 'question-' + question.id}
            />
          )
        })}
      </div>
    </PollQuestionLayout>
  )
}
