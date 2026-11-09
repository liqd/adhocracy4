import { STATES, ACTIONS, isValidTransition } from '../utils/stateMachine'

export const initialState = {
  // Machine state
  state: STATES.LOADING,

  // Navigation
  currentQuestionIndex: 0,

  // Data
  questions: [],
  userAnswers: {},
  results: [],

  // Permissions & Settings
  allowUnregisteredUsers: false,
  guestCanVote: false,
  canVote: false,
  isAuthenticated: false,
  hasUserVote: false,
  isReadOnly: false,
  votingEnded: false,
  useTermsOfUse: false,
  agreedTermsOfUse: false,
  orgTermsUrl: '',

  // UI State
  alert: null,
  checkedTermsOfUse: false,
  errors: {},
  isLoading: true,
  isSubmitting: false,

  // Participants
  totalParticipants: 0,

  // Module info
  moduleName: '',
  moduleDescription: '',

  // Result visibility
  hideResultsUntilFinished: false,

  // Captcha
  captcha: '',
  refreshCaptcha: 0,
  captchaEnabled: false
}

const reducers = {
  [ACTIONS.DATA_LOADED]: (state, payload) => ({
    ...state,
    questions: payload.questions,
    userAnswers: payload.userAnswers,
    results: payload.results,
    allowUnregisteredUsers: payload.allowUnregisteredUsers,
    guestCanVote: payload.guestCanVote,
    canVote: payload.canVote,
    isAuthenticated: payload.isAuthenticated,
    hasUserVote: payload.hasUserVote,
    isReadOnly: payload.isReadOnly,
    votingEnded: payload.votingEnded,
    useTermsOfUse: payload.useTermsOfUse,
    agreedTermsOfUse: payload.agreedTermsOfUse,
    orgTermsUrl: payload.orgTermsUrl,
    totalParticipants: payload.totalParticipants,
    moduleName: payload.moduleName,
    moduleDescription: payload.moduleDescription,
    hideResultsUntilFinished: payload.hideResultsUntilFinished,
    captchaEnabled: payload.captchaEnabled,
    state: (payload.hasUserVote || payload.votingEnded) ? STATES.RESULTS : STATES.START_SCREEN,
    isLoading: false
  }),

  [ACTIONS.DATA_ERROR]: (state, payload) => ({
    ...state,
    state: STATES.ERROR,
    alert: payload,
    isLoading: false
  }),

  [ACTIONS.START_POLL]: (state) => ({
    ...state,
    state: STATES.ANSWERING,
    currentQuestionIndex: 0,
    alert: null
  }),

  [ACTIONS.NEXT_QUESTION]: (state) => {
    if (state.currentQuestionIndex >= state.questions.length - 1) return state
    return {
      ...state,
      currentQuestionIndex: state.currentQuestionIndex + 1,
      alert: null
    }
  },

  [ACTIONS.PREV_QUESTION]: (state) => {
    if (state.currentQuestionIndex <= 0) return state
    return {
      ...state,
      currentQuestionIndex: state.currentQuestionIndex - 1,
      alert: null
    }
  },

  [ACTIONS.SKIP_QUESTION]: (state) => {
    if (state.currentQuestionIndex >= state.questions.length - 1) return state
    const currentQuestionId = state.questions[state.currentQuestionIndex].id
    const updatedAnswers = { ...state.userAnswers }
    delete updatedAnswers[currentQuestionId]
    return {
      ...state,
      currentQuestionIndex: state.currentQuestionIndex + 1,
      userAnswers: updatedAnswers,
      alert: null
    }
  },

  [ACTIONS.UPDATE_ANSWER]: (state, { questionId, answerData }) => ({
    ...state,
    userAnswers: {
      ...state.userAnswers,
      [questionId]: {
        ...state.userAnswers[questionId],
        ...answerData
      }
    }
  }),

  [ACTIONS.SUBMIT_START]: (state) => ({
    ...state,
    state: STATES.SUBMITTING,
    isSubmitting: true,
    checkedTermsOfUse: false
  }),

  [ACTIONS.SUBMIT_SUCCESS]: (state, payload) => ({
    ...state,
    state: STATES.RESULTS,
    results: payload.results,
    questions: payload.questions,
    hasUserVote: true,
    isReadOnly: payload.questions?.length > 0 && !!payload.questions[0]?.isReadOnly,
    votingEnded: !!payload.votingEnded,
    useTermsOfUse: payload.useTermsOfUse,
    agreedTermsOfUse: payload.agreedTermsOfUse,
    orgTermsUrl: payload.orgTermsUrl,
    totalParticipants: payload.totalParticipants,
    hideResultsUntilFinished: payload.hideResultsUntilFinished,
    isSubmitting: false,
    alert: payload.alert
  }),

  [ACTIONS.SUBMIT_ERROR]: (state, payload) => ({
    ...state,
    state: STATES.ANSWERING,
    isSubmitting: false,
    alert: payload,
    refreshCaptcha: state.refreshCaptcha + 1
  }),

  [ACTIONS.SET_ALERT]: (state, payload) => ({
    ...state,
    alert: payload
  }),

  [ACTIONS.CLEAR_ALERT]: (state) => ({
    ...state,
    alert: null
  }),

  [ACTIONS.SET_CHECKED_TERMS]: (state, payload) => ({
    ...state,
    checkedTermsOfUse: payload
  }),

  [ACTIONS.SET_CAPTCHA]: (state, payload) => ({
    ...state,
    captcha: payload
  }),

  [ACTIONS.BACK_TO_POLL]: (state) => ({
    ...state,
    state: STATES.START_SCREEN,
    currentQuestionIndex: 0
  }),

  [ACTIONS.CHANGE_ANSWER]: (state) => ({
    ...state,
    state: STATES.ANSWERING,
    currentQuestionIndex: 0
  }),

  [ACTIONS.SHOW_RESULTS]: (state) => ({
    ...state,
    state: STATES.RESULTS
  })
}

export const pollReducer = (state, action) => {
  if (!isValidTransition(state.state, action.type)) {
    return state
  }

  const reducer = reducers[action.type]
  if (!reducer) {
    return state
  }

  return reducer(state, action.payload)
}
