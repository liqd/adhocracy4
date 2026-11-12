import React, { useState, useCallback, useMemo } from 'react'
import django from 'django'

import { ChoiceRow } from './ChoiceRow'
import QuestionImage from './QuestionImage'

const PollQuestionSlider = ({ answers, isUserAnswer }) => {
  const [currentSlide, setCurrentSlide] = useState(0)
  const total = answers.length
  const current = answers[currentSlide]

  return (
    <div className="poll-slider">
      <div
        className="poll-slider__item"
        role="group"
        aria-label={django.interpolate(
          django.gettext('Answer %(current)s of %(total)s'),
          { current: currentSlide + 1, total },
          true
        )}
      >
        <div className="poll-slider__answer">
          {isUserAnswer(current) && (
            <span
              className="poll-slider__answer-icon"
              role="img"
              aria-label={django.gettext('Your answer')}
            >
              <i className="fas fa-check" aria-hidden="true" />
            </span>
          )}
          <span>{current.answer}</span>
        </div>
      </div>
      <div className="poll-slider__footer">
        <span className="poll-slider__count">{(currentSlide + 1) + '/' + total}</span>
        <div className="poll-slider__nav">
          <button
            type="button"
            onClick={() => setCurrentSlide((slide) => Math.max(0, slide - 1))}
            disabled={currentSlide === 0}
            aria-label={django.gettext('Previous answer')}
          >
            <i className="fa-solid fa-chevron-left" aria-hidden="true" />
          </button>
          <button
            type="button"
            onClick={() => setCurrentSlide((slide) => Math.min(total - 1, slide + 1))}
            disabled={currentSlide === total - 1}
            aria-label={django.gettext('Next answer')}
          >
            <i className="fa-solid fa-chevron-right" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  )
}

const OtherAnswersSection = ({
  otherAnswers,
  isUserAnswer,
  showOtherAnswers,
  onToggle
}) => {
  if (!otherAnswers?.length) return null

  return (
    <div className="poll-result-other-section">
      <button
        type="button"
        className="btn poll__btn--link"
        onClick={onToggle}
      >
        {showOtherAnswers ? django.gettext('Hide other answers') : django.gettext('Show other answers')}
      </button>

      {showOtherAnswers && (
        <div className="poll-result-other-section__slider">
          <PollQuestionSlider answers={otherAnswers} isUserAnswer={isUserAnswer} />
        </div>
      )}
    </div>
  )
}

const PollResult = ({ question }) => {
  const [showOtherAnswers, setShowOtherAnswers] = useState(false)

  const userAnswerId = useMemo(() => {
    return question.is_open
      ? question.userAnswer
      : question.other_choice_user_answer
  }, [question])

  const isUserAnswer = useCallback((slide) => {
    const matchedId = question.is_open
      ? slide.id === userAnswerId
      : slide.vote_id === userAnswerId
    return !!matchedId
  }, [question.is_open, userAnswerId])

  const handleToggleOtherAnswers = useCallback(() => {
    setShowOtherAnswers((prev) => !prev)
  }, [])

  const getHelpText = useMemo(() => {
    if (question.is_confidential) {
      const total = question.is_open ? question.totalAnswerCount : question.totalVoteCount
      return django.interpolate(
        django.ngettext('%s response submitted', '%s responses submitted', total ?? 0),
        [total ?? 0]
      )
    }

    if (question.is_open) {
      const total = question.totalAnswerCount ?? 0
      return total >= 1
        ? django.interpolate(django.ngettext('1 person has answered.', '%s people have answered.', total), [total])
        : django.gettext('no one has answered this question')
    }

    const total = question.totalVoteCount ?? 0
    const totalMulti = question.totalVoteCountMulti ?? 0

    if (question.multiple_choice) {
      const participantText = total === 1 && totalMulti === 1
        ? django.gettext('%s participant gave 1 answer.')
        : django.ngettext('%s participant gave %s answers.', '%s participants gave %s answers.', total)

      return django.interpolate(
        participantText + django.gettext(' For multiple choice questions the percentages may add up to more than 100%.'),
        [total, totalMulti]
      )
    }

    return django.interpolate(
      django.ngettext('1 person has answered.', '%s people have answered.', total),
      [total]
    )
  }, [question])

  // Confidential question view
  if (question.is_confidential) {
    return (
      <div className="poll poll--result poll--confidential">
        <h2>{question.label}</h2>
        {question.image_url && <QuestionImage imageUrl={question.image_url} alt={question.image_alt_text || question.label} />}
        <div className="a4-muted">{getHelpText}</div>
        <p className="poll__confidential-notice">
          <i className="fa fa-lock" aria-hidden="true" />{' '}
          {django.gettext('Answers to this question will be visible only to the initiators of this project.')}
        </p>
      </div>
    )
  }

  const totalVotes = question.totalVoteCount ?? 0

  return (
    <div className="poll poll--result">
      <h2>{question.label}</h2>
      {question.image_url && <QuestionImage imageUrl={question.image_url} alt={question.image_alt_text || question.label} />}

      <div className="poll__rows">
        {/* Non-open questions - reuse ChoiceRow */}
        {!question.is_open && question.choices.map((choice) => {
          const isChosen = (question.userChoices || []).includes(choice.id)
          const percent = totalVotes === 0 ? 0 : Math.round(((choice.count ?? 0) / totalVotes) * 100)

          return (
            <div key={choice.id}>
              <ChoiceRow
                choice={choice}
                checked={isChosen}
                type={question.multiple_choice ? 'checkbox' : 'radio'}
                isResult
                percent={percent}
                disabled
              />

              {/* Other answers section */}
              {choice.is_other_choice && (
                <OtherAnswersSection
                  otherAnswers={question.other_choice_answers}
                  isUserAnswer={isUserAnswer}
                  showOtherAnswers={showOtherAnswers}
                  onToggle={handleToggleOtherAnswers}
                />
              )}
            </div>
          )
        })}

        {/* Open questions */}
        {question.is_open && (question.answers?.length ?? 0) > 0 && (
          <PollQuestionSlider answers={question.answers} isUserAnswer={isUserAnswer} />
        )}

        {/* Help text */}
        <div className="a4-muted">{getHelpText}</div>
      </div>
    </div>
  )
}

export default PollResult
