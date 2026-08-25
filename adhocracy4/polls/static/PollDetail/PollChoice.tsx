import React, { useEffect, useState } from 'react'
import django from 'django'
import { ChoiceRow } from './ChoiceRow'
import { PollQuestionLayout } from './PollQuestionLayout'
import type { PollAnswer, PollChoice as PollChoiceType, PollQuestion } from '../../../static/api/types'
const translated = {
  multiple: django.gettext('Multiple answers are possible.')
}

interface PollChoiceProps {
  question: PollQuestion
  allowUnregisteredUsers: boolean
  onSingleChange: (questionId: number | string, choiceId: number) => void
  onMultiChange: (questionId: number | string, choiceId: number) => void
  onOtherChange: (questionId: number | string, otherAnswer: string, otherChoice?: PollChoiceType) => void
  errors: Record<string, string[]> | undefined
  questionImagesEnabled?: boolean
}

export const PollChoice = ({
  question,
  allowUnregisteredUsers,
  onSingleChange,
  onMultiChange,
  onOtherChange,
  errors,
  questionImagesEnabled
}: PollChoiceProps) => {
  const getUserAnswer = () => {
    const userAnswerId = question.other_choice_user_answer
    const userAnswer = question.other_choice_answers.find((oc: PollAnswer) => oc.vote_id === userAnswerId)
    return question.other_choice_answer
      ? question.other_choice_answer
      : ((userAnswerId && userAnswer)
          ? userAnswer.answer
          : ''
        )
  }

  const [userChoices, setUserChoices] = useState<number[]>([])
  const [otherChoiceAnswer, setOtherChoiceAnswer] = useState<string>(getUserAnswer())

  const multiHelpText = question.multiple_choice ? <div className="poll__help-text">{translated.multiple}</div> : null
  const userAllowedVote = question.authenticated || allowUnregisteredUsers

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    setUserChoices(question.userChoices || [])
  }, [question.userChoices])
  /* eslint-enable react-hooks/set-state-in-effect */

  const findOtherChoice = () => {
    return question.choices.find((c: PollChoiceType) => c.is_other_choice)
  }

  const handleSingleChange = (event: React.ChangeEvent<HTMLInputElement>, isOther: boolean) => {
    const choiceId = parseInt(event.target.value)
    setUserChoices([choiceId])
    onSingleChange(question.id, choiceId)
    if (!isOther) {
      setOtherChoiceAnswer('')
      onOtherChange(question.id, '', findOtherChoice())
    }
  }

  const handleMultiChange = (event: React.ChangeEvent<HTMLInputElement>, _isOther: boolean) => {
    const choiceId = parseInt(event.target.value)
    const newChoices = userChoices.includes(choiceId)
      ? userChoices.filter(id => id !== choiceId)
      : [...userChoices, choiceId]

    setUserChoices(newChoices)
    onMultiChange(question.id, choiceId)

    const otherChoice = findOtherChoice()
    if (!newChoices.includes(otherChoice?.id as number)) {
      setOtherChoiceAnswer('')
      onOtherChange(question.id, '', otherChoice)
    }
  }

  const handleOtherChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const otherAnswer = event.target.value
    setOtherChoiceAnswer(otherAnswer)
    onOtherChange(question.id, otherAnswer)
  }

  return (
    <PollQuestionLayout question={question} questionImagesEnabled={questionImagesEnabled}>
      {multiHelpText}
      <div className="poll__rows">
        {question.choices.map((choice: PollChoiceType) => {
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