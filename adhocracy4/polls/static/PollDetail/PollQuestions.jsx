import React, { useReducer, useMemo, useEffect } from 'react'
import django from 'django'

import Alert from '../../../static/Alert'
import Captcha from '../../../static/Captcha'
import StartScreen from './StartScreen'
import QuestionFunnel from './QuestionFunnel'
import PollLongform from './PollLongform'
import ResultsView from './ResultsView'
import PollAnswerReview from './PollAnswerReview'
import { LoadingSpinner } from './LoadingSpinner'
import { usePollData } from './hooks/usePollData'
import { usePollActions } from './hooks/usePollActions'
import { pollReducer, initialState } from './reducers/pollReducer'
import { STATES } from './utils/stateMachine'

const PollQuestions = ({
  pollId,
  captchaUrl,
  questionImagesEnabled,
  manualLink
}) => {
  const [state, dispatch] = useReducer(pollReducer, initialState)
  const captchaEnabled = Boolean(captchaUrl)

  usePollData(pollId, dispatch, captchaEnabled)

  const actions = usePollActions(state, dispatch, pollId)

  const currentQuestion = useMemo(
    () => state.questions[state.currentQuestionIndex],
    [state.questions, state.currentQuestionIndex]
  )

  const currentAnswer = useMemo(
    () => currentQuestion ? state.userAnswers[currentQuestion.id] : null,
    [currentQuestion, state.userAnswers]
  )

  const showCaptcha = captchaEnabled &&
    state.allowUnregisteredUsers &&
    !state.isAuthenticated

  const canChangeAnswer = state.isAuthenticated && !state.isReadOnly && state.canVote

  useEffect(() => {
    if (state.state === STATES.ANSWERING || state.state === STATES.SUBMITTING) {
      document.body.classList.add('poll-answering')
    } else {
      document.body.classList.remove('poll-answering')
    }
  }, [state.state])

  useEffect(() => {
    if (state.state === STATES.RESULTS) {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }, [state.state])

  useEffect(() => {
    const cta = document.querySelector('[data-poll-cta]')
    if (!cta) return undefined

    const canParticipate = state.canVote
    const isStart = state.state === STATES.START_SCREEN
    const isResults = state.state === STATES.RESULTS

    cta.hidden = !canParticipate ||
      !(isStart || (isResults && (!state.hasUserVote || canChangeAnswer)))
    if (isStart) cta.textContent = django.gettext('Start poll')
    if (isResults) {
      cta.textContent = state.hasUserVote
        ? django.gettext('Change answer')
        : django.gettext('Start poll')
    }

    const handler = () => {
      if (isStart) actions.handleStartPoll()
      if (isResults) actions.handleChangeAnswer()
    }
    cta.addEventListener('click', handler)
    return () => cta.removeEventListener('click', handler)
  }, [state.state, state.canVote, state.hasUserVote, state.isAuthenticated, state.isReadOnly, actions])

  const hasPhaseCta = typeof document !== 'undefined' && !!document.querySelector('[data-poll-cta]')

  const renderStateContent = () => {
    switch (state.state) {
      case STATES.LOADING:
        return <LoadingSpinner />

      case STATES.ERROR:
        return (
          <div className="alert alert-danger" role="alert">
            {django.gettext('Failed to load poll data. Please try again.')}
          </div>
        )

      case STATES.RESULTS:
        if (!state.hideResultsUntilFinished || state.votingEnded) {
          return (
            <ResultsView
              results={state.results}
              totalParticipants={state.totalParticipants}
              hasUserVote={state.hasUserVote}
              votingEnded={state.votingEnded}
              canChangeAnswer={canChangeAnswer}
              alert={state.alert}
              onBackToPoll={actions.handleBackToPoll}
              onChangeAnswer={actions.handleChangeAnswer}
            />
          )
        }

        return (
          <PollAnswerReview
            questions={state.questions}
            canChangeAnswer={canChangeAnswer}
            onChangeAnswer={actions.handleChangeAnswer}
          />
        )

      case STATES.START_SCREEN:
        return (
          <StartScreen
            totalQuestions={state.questions.length}
            totalParticipants={state.totalParticipants}
            isAuthenticated={state.isAuthenticated}
            allowUnregisteredUsers={state.allowUnregisteredUsers}
            canVote={state.canVote}
            hideResultsUntilFinished={state.hideResultsUntilFinished}
            manualLink={manualLink}
            onStart={actions.handleStartPoll}
            onShowResults={actions.handleShowResults}
            hideStartButton={hasPhaseCta}
          />
        )

      case STATES.SUBMITTING:
      case STATES.ANSWERING: {
        const captcha = showCaptcha && (
          <Captcha
            key={state.refreshCaptcha}
            onChange={actions.handleSetCaptcha}
            apiUrl={captchaUrl}
            name="id_captcheck"
            refresh={state.refreshCaptcha}
          />
        )

        return (
          <div className="pollquestionlist-container">
            <form onSubmit={(e) => e.preventDefault()}>
              {state.presentationMode === 'longform'
                ? (
                  <PollLongform
                    questions={state.questions}
                    answers={state.userAnswers}
                    allowUnregisteredUsers={state.allowUnregisteredUsers}
                    questionImagesEnabled={questionImagesEnabled}
                    errors={state.errors}
                    useTermsOfUse={state.useTermsOfUse}
                    agreedTermsOfUse={state.agreedTermsOfUse}
                    orgTermsUrl={state.orgTermsUrl}
                    checkedTermsOfUse={state.checkedTermsOfUse}
                    onSetCheckedTerms={actions.handleSetCheckedTerms}
                    showCaptcha={showCaptcha}
                    captcha={state.captcha}
                    onAnswerChange={actions.handleAnswerChange}
                    onSubmit={actions.handleSubmitAll}
                    isLoading={state.isSubmitting}
                  >
                    {captcha}
                  </PollLongform>
                  )
                : (
                  <QuestionFunnel
                    currentQuestion={currentQuestion}
                    currentAnswer={currentAnswer}
                    currentNumber={state.currentQuestionIndex + 1}
                    totalQuestions={state.questions.length}
                    allowUnregisteredUsers={state.allowUnregisteredUsers}
                    errors={state.errors}
                    onAnswerChange={actions.handleAnswerChange}
                    onBack={actions.handleBack}
                    onSkip={actions.handleSkip}
                    onNext={actions.handleNext}
                    onSubmit={actions.handleSubmitAll}
                    isLoading={state.isSubmitting}
                    useTermsOfUse={state.useTermsOfUse}
                    agreedTermsOfUse={state.agreedTermsOfUse}
                    orgTermsUrl={state.orgTermsUrl}
                    checkedTermsOfUse={state.checkedTermsOfUse}
                    onSetCheckedTerms={actions.handleSetCheckedTerms}
                    showCaptcha={showCaptcha}
                    captcha={state.captcha}
                    questionImagesEnabled={questionImagesEnabled}
                  >
                    {captcha}
                  </QuestionFunnel>
                  )}
            </form>

            {state.alert && (
              <Alert onClick={actions.handleClearAlert} {...state.alert} />
            )}
          </div>
        )
      }
    }
  }

  return renderStateContent()
}

export default PollQuestions
