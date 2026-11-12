import React from 'react'

import { PollChoice } from './PollChoice'
import { PollOpenQuestion } from './PollOpenQuestion'

const ANSWER_HANDLERS = {
  single: (value) => ({ choices: [Number(value)] }),
  multi: (value, currentChoices = []) => {
    const val = Number(value)
    return {
      choices: currentChoices.includes(val)
        ? currentChoices.filter((choice) => choice !== val)
        : [...currentChoices, val]
    }
  },
  open: (value) => ({ open_answer: String(value) }),
  other: (value) => ({ other_choice_answer: String(value) })
}

export const enrichQuestion = (question, answer) => ({
  ...question,
  userChoices: answer?.choices || [],
  open_answer: answer?.open_answer ?? question.open_answer,
  other_choice_answer: answer?.other_choice_answer ?? question.other_choice_answer
})

/**
 * Renders a single poll question with its input. Used by both the multistep
 * funnel and the longform, so both presentations share the same markup.
 */
export const PollQuestion = ({
  question,
  answer,
  allowUnregisteredUsers,
  questionImagesEnabled,
  errors,
  disabled = false,
  onAnswerChange
}) => {
  const enrichedQuestion = {
    ...enrichQuestion(question, answer),
    // Keep the question read-only while a submission is pending or the
    // question is animating out.
    isReadOnly: Boolean(question.isReadOnly || disabled)
  }

  const handleAnswerUpdate = (questionId, value, type) => {
    const handler = ANSWER_HANDLERS[type]
    if (!handler) return

    const currentChoices = answer?.choices || []
    onAnswerChange(questionId, handler(value, currentChoices))
  }

  if (question.is_open) {
    return (
      <PollOpenQuestion
        allowUnregisteredUsers={allowUnregisteredUsers}
        question={enrichedQuestion}
        errors={errors}
        questionImagesEnabled={questionImagesEnabled}
        onOpenChange={disabled
          ? () => {}
          : (questionId, value) => handleAnswerUpdate(questionId, value, 'open')}
      />
    )
  }

  return (
    <PollChoice
      allowUnregisteredUsers={allowUnregisteredUsers}
      question={enrichedQuestion}
      errors={errors}
      questionImagesEnabled={questionImagesEnabled}
      onAnswerChange={disabled ? () => {} : handleAnswerUpdate}
    />
  )
}
