import React, { useState, useCallback, useEffect, useLayoutEffect, useRef } from 'react'
import django from 'django'

import { TermsOfUseCheckbox } from '../../../static/TermsOfUseCheckbox'
import { PollQuestion } from './PollQuestion'
import ProgressBar from './ProgressBar'
import NavigationButtons from './NavigationButtons'

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
    // Measure after the browser settled the new layout (e.g. content above the
    // funnel hiding), otherwise the progress bar ends up outside the viewport.
    let frame
    let timeout
    const scrollToFunnel = (behavior) => {
      if (!funnelRef.current) return
      const top = funnelRef.current.getBoundingClientRect().top + window.scrollY - 100
      window.scrollTo({ top: Math.max(top, 0), behavior })
    }

    frame = window.requestAnimationFrame(() => {
      frame = window.requestAnimationFrame(() => {
        scrollToFunnel('smooth')
        headerRef.current?.focus({ preventScroll: true })
        // Sticky headers may collapse while scrolling and shift the content.
        // Correct small offsets once the smooth scroll has settled, but never
        // fight a user who already scrolled away.
        timeout = window.setTimeout(() => {
          if (!funnelRef.current) return
          const offset = funnelRef.current.getBoundingClientRect().top - 100
          if (Math.abs(offset) > 2 && Math.abs(offset) < 80) {
            scrollToFunnel('smooth')
          }
        }, 450)
      })
    })

    return () => {
      window.cancelAnimationFrame(frame)
      window.clearTimeout(timeout)
    }
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

  const isLastQuestion = currentNumber === totalQuestions
  const isSubmitDisabled = (isLastQuestion && useTermsOfUse && !agreedTermsOfUse && !checkedTermsOfUse) ||
    (isLastQuestion && showCaptcha && !captcha)

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
              <PollQuestion
                question={exitingQuestion}
                answer={exitingAnswer}
                allowUnregisteredUsers={allowUnregisteredUsers}
                questionImagesEnabled={questionImagesEnabled}
                errors={errors}
                disabled
              />
            </div>
            )
          : (
            <div
              className={'poll-question-content poll-question-content--enter-' + direction}
              onAnimationEnd={phase === 'entering' ? handleEnterEnd : undefined}
            >
              <PollQuestion
                question={currentQuestion}
                answer={currentAnswer}
                allowUnregisteredUsers={allowUnregisteredUsers}
                questionImagesEnabled={questionImagesEnabled}
                errors={errors}
                disabled={isLoading}
                onAnswerChange={onAnswerChange}
              />
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
