import React, { useState } from 'react'
import { TextareaWithCounter } from './TextareaWithCounter'
import { PollQuestionLayout } from './PollQuestionLayout'
import type { PollAnswer, PollQuestion } from '../../../static/api/types'

interface PollOpenQuestionProps {
  question: PollQuestion
  allowUnregisteredUsers: boolean
  onOpenChange: (questionId: number | string, value: string) => void
  errors: Record<string, string[]> | undefined
  questionImagesEnabled?: boolean
}

export const PollOpenQuestion = ({
  question,
  allowUnregisteredUsers,
  onOpenChange,
  errors,
  questionImagesEnabled
}: PollOpenQuestionProps) => {
  const getUserOpenAnswer = () => {
    const userAnswerId = question.userAnswer
    const userAnswer = question.answers.find((oa: PollAnswer) => oa.id === userAnswerId)
    return question.open_answer
      ? question.open_answer
      : userAnswerId && userAnswer
        ? userAnswer.answer
        : ''
  }

  const [userAnswer, setUserAnswer] = useState<string>(getUserOpenAnswer())
  const userAllowedVote = question.authenticated || allowUnregisteredUsers

  const handleOpenChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
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