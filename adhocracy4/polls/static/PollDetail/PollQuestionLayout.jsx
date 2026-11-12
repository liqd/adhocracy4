import React from 'react'
import { ConfidentialNotice } from './ConfidentialNotice'
import QuestionImage from './QuestionImage'

export const PollQuestionLayout = ({ question, questionImagesEnabled, children }) => {
  return (
    <div className="poll poll--question" data-testid="poll-open-question">
      <fieldset>
        <legend className="poll__question-legend">
          <span className="poll__question-label">{question.label}</span>
        </legend>
        {question.help_text && (
          <div className="poll__help-text">{question.help_text}</div>
        )}
        {questionImagesEnabled && question.image_url && (
          <QuestionImage
            imageUrl={question.image_url}
            alt={question.image_alt_text || question.label}
          />
        )}
        {question.is_confidential && <ConfidentialNotice />}
        {children}
      </fieldset>
    </div>
  )
}
