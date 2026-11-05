import React, { useState } from 'react'
import django from 'django'

import Alert from '../../../static/Alert'
import { ChoiceRow } from './ChoiceRow'
import { ConfidentialNotice } from './ConfidentialNotice'
import QuestionImage from './QuestionImage'

const PollAnswerReview = ({ questions, onChangeAnswer, hideChangeButton }) => {
  const [bannerDismissed, setBannerDismissed] = useState(false)

  return (
    <div className="poll-answer-review">
      <div className="poll-answer-review__banner">
        {!bannerDismissed && (
          <Alert
            type="info"
            message={django.gettext(
              'Thank you for taking part in the poll! You will see the results as soon as the participation phase is over.'
            )}
            onClick={() => setBannerDismissed(true)}
          />
        )}
      </div>

      {questions.map((question) => (
        <div className="poll poll--question" key={question.id}>
          <fieldset>
            <legend className="poll__question-legend">
              <span className="poll__question-label">{question.label}</span>
            </legend>

            {question.image_url && (
              <QuestionImage
                imageUrl={question.image_url}
                alt={question.image_alt_text || question.label}
              />
            )}

            {question.help_text && (
              <div className="poll__help-text">{question.help_text}</div>
            )}

            {question.is_confidential && <ConfidentialNotice />}

            <div className="poll__rows">
              {!question.is_open &&
                question.choices.map((choice) => {
                  const isChosen = (question.userChoices || []).includes(choice.id)
                  const ownOtherAnswer =
                    choice.is_other_choice && question.other_choice_user_answer
                      ? question.other_choice_answers?.find(
                        (answer) => answer.vote_id === question.other_choice_user_answer
                      )?.answer
                      : null

                  return (
                    <div key={choice.id}>
                      <ChoiceRow
                        choice={choice}
                        checked={isChosen}
                        type={question.multiple_choice ? 'checkbox' : 'radio'}
                        isResult
                        review
                        disabled
                      />
                      {ownOtherAnswer && (
                        <div className="poll-answer-review__other-answer">
                          {ownOtherAnswer}
                        </div>
                      )}
                    </div>
                  )
                })}

              {question.is_open && (
                <div className="poll-answer-review__open-answer">
                  {question.answers?.find((answer) => answer.id === question.userAnswer)?.answer ||
                    django.gettext('No answer given.')}
                </div>
              )}
            </div>
          </fieldset>
        </div>
      ))}

      {!hideChangeButton && (
        <div className="poll-answer-review__buttons">
          <button
            type="button"
            className="btn btn--transparent-bordered"
            onClick={onChangeAnswer}
          >
            {django.gettext('Change my answers')}
          </button>
        </div>
      )}
    </div>
  )
}

export default PollAnswerReview
