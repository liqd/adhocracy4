import { useEffect } from 'react'
import api from '../../../../static/api'
import django from 'django'

const normalizePollData = (poll, captchaEnabled) => {
  const userAnswers = {}

  poll.questions.forEach((question) => {
    const hasUserChoices = !!question.userChoices?.length

    // Open question: API provides answers[] + userAnswer (Answer ID), not a flat open_answer field
    const existingOpenAnswer = question.is_open && question.userAnswer
      ? question.answers?.find((answer) => answer.id === question.userAnswer)?.answer || ''
      : (question.open_answer || '')

    const hasOpenAnswer = existingOpenAnswer !== ''

    // Choice question with "other": API provides other_choice_answers[] + other_choice_user_answer (Vote ID)
    const existingOtherAnswer = !question.is_open && question.other_choice_user_answer
      ? question.other_choice_answers?.find((answer) => answer.vote_id === question.other_choice_user_answer)?.answer || ''
      : (question.other_choice_answer || '')

    if (hasUserChoices || hasOpenAnswer) {
      userAnswers[question.id] = {
        choices: question.userChoices || [],
        open_answer: existingOpenAnswer,
        other_choice_answer: existingOtherAnswer
      }
    }
  })

  const firstQuestion = poll.questions[0]
  const isAuthenticated = !!firstQuestion?.authenticated
  const isReadOnly = !!firstQuestion?.isReadOnly

  return {
    questions: poll.questions,
    userAnswers,
    results: JSON.parse(JSON.stringify(poll.questions)),
    allowUnregisteredUsers: poll.allow_unregistered_users,
    presentationMode: poll.presentation_mode || 'multistep',
    guestCanVote: poll.guest_can_vote,
    canVote: !!poll.can_vote,
    isAuthenticated,
    hasUserVote: poll.has_user_vote,
    isReadOnly,
    votingEnded: !!poll.voting_ended,
    useTermsOfUse: poll.use_org_terms_of_use,
    agreedTermsOfUse: poll.user_has_agreed,
    orgTermsUrl: poll.org_terms_url,
    totalParticipants: poll.total_participants || 0,
    moduleName: poll.module_name || '',
    moduleDescription: poll.module_description || '',
    hideResultsUntilFinished: poll.hide_results_until_finished || false,
    captchaEnabled
  }
}

export const usePollData = (pollId, dispatch, captchaEnabled) => {
  useEffect(() => {
    if (!pollId) return

    api.poll.get(pollId)
      .done((poll) => {
        dispatch({
          type: 'DATA_LOADED',
          payload: normalizePollData(poll, captchaEnabled)
        })
      })
      .fail(() => {
        dispatch({
          type: 'DATA_ERROR',
          payload: {
            type: 'danger',
            message: django.gettext('Failed to load poll data. Please try again.')
          }
        })
      })
  }, [pollId, dispatch, captchaEnabled])
}
