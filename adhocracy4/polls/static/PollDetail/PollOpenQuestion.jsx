import React, { useState } from 'react'
import { TextareaWithCounter } from './TextareaWithCounter'
import { PollQuestionLayout } from './PollQuestionLayout'

export const PollOpenQuestion = ({
  question,
  allowUnregisteredUsers,
  onOpenChange,
  errors,
  questionImagesEnabled
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
  const userAllowedVote = question.authenticated || allowUnregisteredUsers

  const handleOpenChange = (event) => {
    setUserAnswer(event.target.value)
    onOpenChange(question.id, event.target.value)
  }

  return (
    <PollQuestionLayout question={question} questionImagesEnabled={questionImagesEnabled}>
      <TextareaWithCounter
        value={userAnswer}
        onChange={handleOpenChange}
        disabled={!userAllowedVote || question.isReadOnly}
        error={errors}
        id={question.id}
        questionType="open"
      />
    </PollQuestionLayout>
  )
}
