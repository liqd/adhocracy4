import React, { useState, useCallback, useEffect, useLayoutEffect, useRef } from 'react'
import django from 'django'

import { TermsOfUseCheckbox } from '../../../static/TermsOfUseCheckbox'
import { PollChoice } from './PollChoice'
import { PollOpenQuestion } from './PollOpenQuestion'
import ProgressBar from './ProgressBar'
import NavigationButtons from './NavigationButtons'

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

const QuestionFunnel = ({
  currentQuestion,
  currentAnswer,
  currentNumber,
  totalQuestions,
  allowUnregisteredUsers,
  useTermsOfUse,
  agreedTermsOfUse,
  orgTermsUrl,
  checkedTermsOfUse,
  showCaptcha,
  captcha,
  onSetCheckedTerms,
  errors,
  onAnswerChange,
  onBack,
  onSkip,
  onNext,
  onSubmit,
  isLoading,
  questionImagesEnabled,
  children
}) => {
  const funnelRef = useRef(null)
  const headerRef = useRef(null)
  const prevNumberRef = useRef(currentNumber)
  const prevQuestionRef = useRef(null)
  const prevAnswerRef = useRef(null)

  const [phase, setPhase] = useState('idle')
  const [direction, setDirection] = useState('forward')
  const [exitingQuestion, setExitingQuestion] = useState(null)
  const [exitingAnswer, setExitingAnswer] = useState(null)

  useLayoutEffect(() => {
    const top = (funnelRef.current?.getBoundingClientRect().top || 0) + window.scrollY - 100
    window.scrollTo({ top, behavior: 'smooth' })
    headerRef.current?.focus({ preventScroll: true })
  }, [currentQuestion.id])

  useLayoutEffect(() => {
    if (currentNumber !== prevNumberRef.current) {
      const dir = currentNumber > prevNumberRef.current ? 'forward' : 'backward'
      setDirection(dir)
      setExitingQuestion(prevQuestionRef.current)
      setExitingAnswer(prevAnswerRef.current)
      setPhase('exiting')
      prevNumberRef.current = currentNumber
    }
    prevQuestionRef.current = currentQuestion
    prevAnswerRef.current = currentAnswer
  }, [currentNumber, currentQuestion, currentAnswer])

  const handleExitEnd = useCallback(() => {
    setExitingQuestion(null)
    setExitingAnswer(null)
    setPhase('entering')
  }, [])

  const handleEnterEnd = useCallback(() => {
    setPhase('idle')
  }, [])

  useEffect(() => {
    if (phase !== 'exiting') return undefined
    // Fallback in case the animation is missing or disabled (e.g. reduced
    // motion): without it the funnel would stay on the previous question.
    const timeout = window.setTimeout(handleExitEnd, 400)
    return () => window.clearTimeout(timeout)
  }, [phase, handleExitEnd])

  const enrichQuestion = useCallback((question, answer) => ({
    ...question,
    userChoices: answer?.choices || [],
    open_answer: answer?.open_answer ?? question.open_answer,
    other_choice_answer: answer?.other_choice_answer ?? question.other_choice_answer
  }), [])

  const isLastQuestion = currentNumber === totalQuestions
  const isSubmitDisabled = (isLastQuestion && useTermsOfUse && !agreedTermsOfUse && !checkedTermsOfUse) ||
    (isLastQuestion && showCaptcha && !captcha)

  const handleAnswerUpdate = (questionId, value, type) => {
    const handler = ANSWER_HANDLERS[type]
    if (!handler) return

    const currentChoices = currentAnswer?.choices || []
    onAnswerChange(questionId, handler(value, currentChoices))
  }

  const renderQuestion = (question, answer, interactive = true) => {
    const questionProps = {
      allowUnregisteredUsers,
      question: {
        ...enrichQuestion(question, answer),
        // Also keep the question read-only while the submission is pending.
        isReadOnly: Boolean(question.isReadOnly || !interactive)
      },
      errors,
      questionImagesEnabled
    }

    if (question.is_open) {
      return (
        <PollOpenQuestion
          key={question.id}
          {...questionProps}
          onOpenChange={interactive
            ? (questionId, value) => handleAnswerUpdate(questionId, value, 'open')
            : () => {}}
        />
      )
    }

    return (
      <PollChoice
        key={question.id}
        {...questionProps}
        onAnswerChange={interactive ? handleAnswerUpdate : () => {}}
      />
    )
  }

  return (
    <div className="poll-question-funnel" ref={funnelRef}>
      <ProgressBar current={currentNumber} total={totalQuestions} />

      <div className="poll-question-header" tabIndex={-1} ref={headerRef}>
        {django.interpolate(
          django.gettext('Question %(current)s of %(total)s'),
          { current: currentNumber, total: totalQuestions },
          true
        )}
      </div>

      <div className="poll-question-content-wrapper">
        {phase === 'exiting' && exitingQuestion
          ? (
            <div
              className={'poll-question-content poll-question-content--exit-' + direction}
              onAnimationEnd={handleExitEnd}
            >
              {renderQuestion(exitingQuestion, exitingAnswer, false)}
            </div>
            )
          : (
            <div
              className={'poll-question-content poll-question-content--enter-' + direction}
              onAnimationEnd={phase === 'entering' ? handleEnterEnd : undefined}
            >
              {renderQuestion(currentQuestion, currentAnswer, !isLoading)}
            </div>
            )}
      </div>

      {isLastQuestion && useTermsOfUse && !agreedTermsOfUse && (
        <div className="col-12 mt-4">
          <TermsOfUseCheckbox
            id="terms-of-use"
            checked={checkedTermsOfUse}
            onChange={onSetCheckedTerms}
            orgTermsUrl={orgTermsUrl}
          />
        </div>
      )}

      {isLastQuestion && children}

      <NavigationButtons
        onBack={onBack}
        onSkip={onSkip}
        onNext={onNext}
        onSubmit={onSubmit}
        isLoading={isLoading}
        isLastQuestion={isLastQuestion}
        isSubmitDisabled={isSubmitDisabled}
        currentIndex={currentNumber - 1}
      />
    </div>
  )
}

export default QuestionFunnel
