import React from 'react'
import { ConfidentialNotice } from './ConfidentialNotice'
import QuestionImage from './QuestionImage'

export const PollQuestionLayout = ({ question, questionImagesEnabled, children }) => {
  const questionHelpText = question.help_text
    ? <div className="poll__help-text">{question.help_text}</div>
    : null

  return (
    <div className="poll poll--question">
      <fieldset>
        <legend className="poll__question-legend">
          <h3>{question.label}</h3>
        </legend>
        {questionHelpText}
        {questionImagesEnabled && (
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
