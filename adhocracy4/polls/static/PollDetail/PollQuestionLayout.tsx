import React from 'react'
import { ConfidentialNotice } from './ConfidentialNotice'
import QuestionImage from './QuestionImage'
import type { PollQuestion } from '../../../static/api/types'

interface PollQuestionLayoutProps {
  question: PollQuestion
  questionImagesEnabled?: boolean
  children: React.ReactNode
}

export const PollQuestionLayout = ({ question, questionImagesEnabled, children }: PollQuestionLayoutProps) => {
  const questionHelpText = question.help_text
    ? <div className="poll__help-text">{question.help_text}</div>
    : null

  return (
    <div className="poll poll--question">
      <fieldset>
        <legend className="poll__question-legend">
          <span className="poll__question-label">{question.label}</span>
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