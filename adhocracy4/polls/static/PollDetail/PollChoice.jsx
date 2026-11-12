import React from 'react'
import django from 'django'

import { ChoiceRow } from './ChoiceRow'
import { ConfidentialNotice } from './ConfidentialNotice'
import QuestionImage from './QuestionImage'

const translated = {
  multiple: django.gettext('Multiple answers are possible.'),
  single: django.gettext('Please select only one answer')
}

export const PollChoice = ({
  question,
  allowUnregisteredUsers,
  onAnswerChange,
  errors,
  questionImagesEnabled
}) => {
  const userChoices = question.userChoices || []
  const otherChoiceAnswer = question.other_choice_answer || ''

  const otherChoice = question.choices.find((choice) => choice.is_other_choice)
  const canVote = (question.authenticated || allowUnregisteredUsers) && !question.isReadOnly

  const handleChoiceChange = (choiceId) => {
    if (question.multiple_choice) {
      const newChoices = userChoices.includes(choiceId)
        ? userChoices.filter((id) => id !== choiceId)
        : [...userChoices, choiceId]

      onAnswerChange(question.id, choiceId, 'multi')

      if (otherChoice && !newChoices.includes(otherChoice.id)) {
        onAnswerChange(question.id, '', 'other')
      }
    } else {
      onAnswerChange(question.id, choiceId, 'single')

      if (otherChoice && choiceId !== otherChoice.id) {
        onAnswerChange(question.id, '', 'other')
      }
    }
  }

  const handleOtherChange = (event) => {
    onAnswerChange(question.id, event.target.value, 'other')
  }

  return (
    <div className="poll poll--question">
      <fieldset>
        <legend className="poll__question-legend">
          <span className="poll__question-label">{question.label}</span>
        </legend>

        {questionImagesEnabled && question.image_url && (
          <QuestionImage
            imageUrl={question.image_url}
            alt={question.image_alt_text || question.label}
          />
        )}

        {question.help_text && (
          <div className="poll__help-text">{question.help_text}</div>
        )}

        {question.multiple_choice && (
          <div className="poll__help-text">{translated.multiple}</div>
        )}

        {!question.multiple_choice && (
          <div className="poll__help-text">{translated.single}</div>
        )}

        {question.is_confidential && <ConfidentialNotice />}

        <div className="poll__rows">
          {question.choices.map((choice) => (
            <ChoiceRow
              key={choice.id}
              choice={choice}
              checked={userChoices.includes(choice.id)}
              onInputChange={() => handleChoiceChange(choice.id)}
              type={question.multiple_choice ? 'checkbox' : 'radio'}
              disabled={!canVote}
              otherChoiceAnswer={otherChoiceAnswer}
              onOtherChange={handleOtherChange}
              errors={errors}
              name={question.multiple_choice ? undefined : 'question-' + question.id}
            />
          ))}
        </div>
      </fieldset>
    </div>
  )
}
