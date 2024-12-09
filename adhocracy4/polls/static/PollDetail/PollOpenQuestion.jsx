import React, { useState } from 'react'
import { TextareaWithCounter } from './TextareaWithCounter'

export const PollOpenQuestion = ({
  question,
  allowUnregisteredUsers,
  onOpenChange,
  errors
}) => {
  const getUserOpenAnswer = () => {
    const userAnswerId = question.userAnswer
    const userAnswer = question.answers.find((oa) => oa.id === userAnswerId)
    return question.open_answer
      ? question.open_answer
      : userAnswerId && userAnswer
        ? userAnswer.answer
        : ''
  }

  const [userAnswer, setUserAnswer] = useState(getUserOpenAnswer())
  const questionHelpText = question.help_text
    ? (
      <div className="poll__help-text">{question.help_text}</div>
      )
    : null
  const userAllowedVote = question.authenticated || allowUnregisteredUsers

  const handleOpenChange = (event) => {
    setUserAnswer(event.target.value)
    onOpenChange(question.id, event.target.value)
  }

  return (
    <div className="poll poll--question">
      <h3>{question.label}</h3>
      {questionHelpText}
      <TextareaWithCounter
        value={userAnswer}
        onChange={handleOpenChange}
        disabled={!userAllowedVote || question.isReadOnly}
        error={errors}
        id={question.id}
        questionType="open"
      />
    </div>
  )
}
