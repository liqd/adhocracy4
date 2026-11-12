import React from 'react'
import django from 'django'

import { TermsOfUseCheckbox } from '../../../static/TermsOfUseCheckbox'
import { PollQuestion } from './PollQuestion'

/**
 * Longform presentation: all questions on one page, a single submit at the
 * end and no progress bar. Shares the question markup with the funnel.
 */
const PollLongform = ({
  questions,
  answers,
  allowUnregisteredUsers,
  questionImagesEnabled,
  errors,
  useTermsOfUse,
  agreedTermsOfUse,
  orgTermsUrl,
  checkedTermsOfUse,
  showCaptcha,
  captcha,
  onSetCheckedTerms,
  onAnswerChange,
  onSubmit,
  isLoading,
  children
}) => {
  const isSubmitDisabled = (useTermsOfUse && !agreedTermsOfUse && !checkedTermsOfUse) ||
    (showCaptcha && !captcha)

  return (
    <div className="poll-longform">
      <div className="poll-longform__questions">
        {questions.map((question) => (
          <div className="poll-longform__question" key={question.id}>
            <PollQuestion
              question={question}
              answer={answers[question.id]}
              allowUnregisteredUsers={allowUnregisteredUsers}
              questionImagesEnabled={questionImagesEnabled}
              errors={errors?.[question.id] || errors}
              disabled={isLoading}
              onAnswerChange={onAnswerChange}
            />
          </div>
        ))}
      </div>

      {useTermsOfUse && !agreedTermsOfUse && (
        <div className="col-12 mt-4">
          <TermsOfUseCheckbox
            id="terms-of-use"
            checked={checkedTermsOfUse}
            onChange={onSetCheckedTerms}
            orgTermsUrl={orgTermsUrl}
          />
        </div>
      )}

      {children}

      <div className="poll-longform__actions">
        <button
          type="button"
          className="btn poll__btn--dark"
          onClick={onSubmit}
          disabled={isLoading || isSubmitDisabled}
        >
          {isLoading ? django.gettext('Submitting...') : django.gettext('Submit All')}
        </button>
      </div>
    </div>
  )
}

export default PollLongform
