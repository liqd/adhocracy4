import { useCallback } from 'react'
import { ACTIONS } from '../utils/stateMachine'
import { hasValidAnswer, buildVoteData } from '../utils/pollHelpers'
import {
  ALERT_INVALID,
  ALERT_SUCCESS,
  ALERT_ERROR,
  ALERT_INCOMPLETE,
  ALERT_CAPTCHA_INCOMPLETE
} from '../utils/alerts'
import { usePollSubmission } from './usePollSubmission'

export const usePollActions = (state, dispatch, pollId) => {
  const { submitVotes } = usePollSubmission(pollId)

  const handleStartPoll = useCallback(() => {
    dispatch({ type: ACTIONS.START_POLL })
  }, [dispatch])

  const handleBackToPoll = useCallback(() => {
    dispatch({ type: ACTIONS.BACK_TO_POLL })
  }, [dispatch])

  const handleChangeAnswer = useCallback(() => {
    dispatch({ type: ACTIONS.CHANGE_ANSWER })
  }, [dispatch])

  const handleNext = useCallback(() => {
    const question = state.questions[state.currentQuestionIndex]
    const answer = state.userAnswers[question?.id]

    if (!hasValidAnswer(question, answer)) {
      dispatch({ type: ACTIONS.SET_ALERT, payload: ALERT_INVALID })
      return
    }

    dispatch({ type: ACTIONS.NEXT_QUESTION })
  }, [state.questions, state.currentQuestionIndex, state.userAnswers, dispatch])

  const handleBack = useCallback(() => {
    dispatch({ type: ACTIONS.PREV_QUESTION })
  }, [dispatch])

  const handleSkip = useCallback(() => {
    dispatch({ type: ACTIONS.SKIP_QUESTION })
  }, [dispatch])

  const handleShowResults = useCallback(() => {
    dispatch({ type: ACTIONS.SHOW_RESULTS })
  }, [dispatch])

  const handleSubmitAll = useCallback(async () => {
    const showCaptcha = state.captchaEnabled && state.allowUnregisteredUsers && !state.isAuthenticated
    if (showCaptcha && !state.captcha) {
      dispatch({ type: ACTIONS.SET_ALERT, payload: ALERT_CAPTCHA_INCOMPLETE })
      return
    }

    const allValid = state.questions.every((question) => {
      const answer = state.userAnswers[question.id]
      return !answer || hasValidAnswer(question, answer)
    })
    if (!allValid) {
      dispatch({ type: ACTIONS.SET_ALERT, payload: ALERT_INCOMPLETE })
      return
    }

    dispatch({ type: ACTIONS.SUBMIT_START })

    const voteData = buildVoteData(state.userAnswers)
    const shouldAgreeTerms = state.useTermsOfUse && !state.agreedTermsOfUse && state.checkedTermsOfUse

    const result = await submitVotes(voteData, {
      agreedTermsOfUse: shouldAgreeTerms,
      captcha: state.captcha
    })

    if (result.success) {
      const resultsHidden = result.hideResultsUntilFinished && !result.votingEnded
      dispatch({
        type: ACTIONS.SUBMIT_SUCCESS,
        payload: {
          ...result,
          alert: resultsHidden ? null : ALERT_SUCCESS
        }
      })
    } else {
      dispatch({ type: ACTIONS.SUBMIT_ERROR, payload: ALERT_ERROR })
    }
  }, [state, dispatch, submitVotes])

  const handleAnswerChange = useCallback((questionId, answerData) => {
    dispatch({
      type: ACTIONS.UPDATE_ANSWER,
      payload: { questionId, answerData }
    })
  }, [dispatch])

  const handleClearAlert = useCallback(() => {
    dispatch({ type: ACTIONS.CLEAR_ALERT })
  }, [dispatch])

  const handleSetCheckedTerms = useCallback((checked) => {
    dispatch({ type: ACTIONS.SET_CHECKED_TERMS, payload: checked })
  }, [dispatch])

  const handleSetCaptcha = useCallback((token) => {
    dispatch({ type: ACTIONS.SET_CAPTCHA, payload: token })
  }, [dispatch])

  return {
    handleStartPoll,
    handleBackToPoll,
    handleChangeAnswer,
    handleNext,
    handleBack,
    handleSkip,
    handleShowResults,
    handleSubmitAll,
    handleAnswerChange,
    handleClearAlert,
    handleSetCheckedTerms,
    handleSetCaptcha
  }
}
