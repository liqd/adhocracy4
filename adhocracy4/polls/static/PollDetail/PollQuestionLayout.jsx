import React from 'react'
import django from 'django'
import { ConfidentialNotice } from './ConfidentialNotice'
import QuestionImage from './QuestionImage'

const translated = {
  mandatory: django.gettext('Mandatory question')
}

export const PollQuestionLayout = ({ question, questionImagesEnabled, children }) => {
  const questionHelpText = question.help_text
    ? <div className="poll__help-text">{question.help_text}</div>
    : null

  return (
    <div className="poll poll--question">
      <fieldset>
        <legend className="poll__question-legend">
          <span className="poll__question-label">
            {question.label}
            {question.is_mandatory && (
              <span className="poll__question-required" aria-hidden="true">*</span>
            )}
          </span>
          {question.is_mandatory && <span className="a4-sr-only">{translated.mandatory}</span>}
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
